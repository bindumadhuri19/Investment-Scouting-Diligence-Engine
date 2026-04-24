# Workflow: Analyze Sentiment

## Objective
Compute news sentiment score and identify negative signals from recent media coverage.

## Required Inputs
- `.tmp/{ticker}_news.json` - Must contain array of articles with: title, description, publishedAt, source

## Tools to Execute
1. `tools/fetch_news_sentiment.py` (already executed in fetch_company_data.md, reads cached result)
2. Keyword-based scoring algorithm (executed within this workflow or as separate tool)

## Expected Outputs
- `.tmp/{ticker}_sentiment.json` - Contains:
  - `total_articles`: Count of articles analyzed
  - `negative_count`: Articles containing negative keywords
  - `positive_count`: Articles containing positive keywords
  - `neutral_count`: Remaining articles
  - `sentiment_score`: 0-100 (0=very negative, 50=neutral, 100=very positive)
  - `sentiment_zone`: "green" (>60), "yellow" (40-60), "red" (<40)
  - `flagged_articles`: Array of articles with negative keywords (top 5)
  - `keywords_detected`: Array of specific negative keywords found

## Execution Steps
1. Load `.tmp/{ticker}_news.json`
2. If <5 articles, flag warning "Insufficient news data" and score as N/A
3. For each article (title + description):
   - Scan for negative keywords
   - Scan for positive keywords
   - Classify as negative, positive, or neutral
4. Calculate sentiment_score: `((positive_count - negative_count) / total_articles * 50) + 50`
5. Identify top 5 most concerning articles (negative keywords + recent date)
6. Write results to `.tmp/{ticker}_sentiment.json`

## Negative Keywords (Red Flags)
**Financial distress**:
- "bankruptcy", "insolvent", "default", "debt crisis", "liquidity crisis"

**Legal issues**:
- "lawsuit", "litigation", "settlement", "SEC investigation", "fraud", "class action"

**Accounting concerns**:
- "restatement", "accounting error", "misstatement", "audit issue", "going concern"

**Operational problems**:
- "layoffs", "plant closure", "recall", "safety issue", "regulatory violation"

**Market concerns**:
- "downgrade", "earnings miss", "guidance cut", "weak outlook", "disappointing results"

## Positive Keywords
- "record revenue", "beat expectations", "strong quarter", "market share gain"
- "acquisition", "partnership", "innovation", "buyback", "dividend increase"

## Sentiment Score Interpretation
- **90-100**: Overwhelmingly positive coverage
- **60-89**: Positive tone, bullish sentiment
- **40-59**: Neutral/mixed coverage
- **20-39**: Negative tone, bearish sentiment
- **0-19**: Highly negative, multiple red flags

## Risk Flags Generated
Automatically flag if:
- Sentiment score < 40 → "Negative media sentiment detected"
- >30% of articles contain "lawsuit" or "fraud" → "Legal risk flagged in media"
- >3 articles mention "bankruptcy" or "default" → "Financial distress signals"
- Recent earnings miss + negative coverage → "Market disappointment"

## Error Handling
- **No articles found**: Set score to N/A, flag "Insufficient news data (ticker may be low-profile)"
- **API data missing fields**: Skip malformed articles, analyze remaining
- **All articles neutral**: Score = 50, note "No strong sentiment signals"

## Validation
- Spot-check keyword detection: Manually review 5 articles, verify classification accuracy ≥80%
- Compare sentiment to stock price trend: Negative news should correlate with price decline (directional validation)

## Performance Targets
- **Execution time**: <2 seconds (keyword scanning)
- **Accuracy**: ≥80% correct classification on manual review

## Limitations & Future Improvements
**Current (MVP)**:
- Simple keyword matching (no context understanding)
- Equal weight to all articles (regardless of source credibility)
- No time decay (recent articles weighted same as 30-day-old)

**Future enhancements**:
- ML-based sentiment (BERT, FinBERT model)
- Source weighting (WSJ > random blog)
- Time decay (recent articles weighted 2x)
- Entity recognition (distinguish company from sector news)

## Notes
- NewsAPI returns max 100 articles in free tier; prioritize recent (sort by publishedAt desc)
- Keyword list should evolve based on false positives discovered during analyst review
- Update workflow when finding common misclassifications (e.g., "lawsuit settlement" often positive outcome)
