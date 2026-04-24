# Workflow: Synthesize Analysis

## Objective
Generate AI-powered investment diligence summary using Claude API to synthesize quantitative and qualitative data.

## Required Inputs
- `.tmp/{ticker}_fundamentals.json` - Company basics, financials
- `.tmp/{ticker}_analysis.json` - Risk metrics (Z-Score, debt ratios)
- `.tmp/{ticker}_sentiment.json` - News sentiment analysis
- `.tmp/{ticker}_sec_filings.json` - SEC filing summary (optional)

## Tools to Execute
1. `tools/synthesize_with_claude.py` - LLM-powered synthesis

## Expected Outputs
- `.tmp/{ticker}_synthesis.json` - Contains:
  - `risk_summary`: Paragraph summarizing overall risk profile
  - `red_flags`: Array of specific concerns identified
  - `opportunities`: Array of positive signals (if any)
  - `investment_recommendation`: "BUY", "HOLD", or "SELL"
  - `confidence_score`: 1-10 (10 = high confidence in analysis)
  - `reasoning`: Explanation of recommendation
  - `next_steps`: Suggested further diligence areas

## Execution Steps
1. Load all cached JSON files from `.tmp/{ticker}_*`
2. Structure data into Claude prompt (see template below)
3. Call Claude API with structured prompt
4. Parse Claude response (expect JSON format)
5. Validate response contains required fields
6. Write to `.tmp/{ticker}_synthesis.json`

## Claude Prompt Template

```
You are an expert investment analyst conducting due diligence on {TICKER}.

**Company Data**:
- Market Cap: {market_cap}
- Current Price: {price}
- P/E Ratio: {pe_ratio}
- Debt/Equity: {debt_to_equity}

**Risk Metrics**:
- Altman Z-Score: {zscore} (Zone: {zscore_zone})
- OCF/Net Income: {ocf_ratio}
- Debt Zone: {debt_zone}

**Sentiment Analysis**:
- Sentiment Score: {sentiment_score}/100
- Negative Article %: {negative_pct}%
- Key Concerns: {flagged_keywords}

**Recent News Highlights**:
{top_5_articles}

**SEC Filing Summary**:
{sec_summary}

**Task**: Provide a structured investment analysis in JSON format:

{
  "risk_summary": "2-3 sentence overview of risk profile",
  "red_flags": ["specific concern 1", "specific concern 2", ...],
  "opportunities": ["positive signal 1", "positive signal 2", ...],
  "investment_recommendation": "BUY | HOLD | SELL",
  "confidence_score": 1-10,
  "reasoning": "Explain your recommendation in 3-4 sentences",
  "next_steps": ["Further diligence action 1", "Further diligence action 2"]
}

**Guidelines**:
- Be objective and data-driven
- Flag only legitimate concerns (avoid over-flagging)
- If data is insufficient, note in reasoning
- Confidence score should reflect data quality (incomplete data = lower score)
- Consider all three risk types: financial, sentiment, legal/regulatory
```

## Recommendation Logic (for Claude guidance)
**BUY signals**:
- Z-Score > 3.0 (green) + positive sentiment + strong fundamentals
- Undervalued (low P/E vs. peers) + no red flags

**HOLD signals**:
- Mixed data (some green, some yellow indicators)
- Insufficient data for strong conviction
- Neutral sentiment + average financial health

**SELL signals**:
- Z-Score < 1.8 (red) + negative sentiment
- Multiple red flags (debt, earnings quality, legal issues)
- Deteriorating fundamentals + poor news flow

## Error Handling
- **Claude API failure**: Retry 2x with 5s delay. If all fail, return error JSON with basic rule-based summary
- **API rate limit**: Wait and retry (exponential backoff)
- **Invalid JSON response**: Parse manually or request re-generation
- **Missing input data**: Claude should note "Analysis limited by missing {field}" in reasoning
- **Hallucination detection**: If Claude references data not provided (e.g., makes up revenue numbers), flag for analyst review

## Validation
- **JSON format**: Verify response is valid JSON with all required fields
- **Recommendation consistency**: If red flags > 3 and recommendation = BUY, flag as inconsistent for review
- **Confidence calibration**: If data is 50% missing but confidence = 10, flag as miscalibrated
- **Analyst review required**: All synthesis outputs must be reviewed by human analyst before client delivery

## Quality Thresholds
- **Acceptable**: Confidence ≥ 6, red_flags align with quantitative data
- **Needs review**: Confidence < 6, or contradictory signals (e.g., Z-Score green but recommends SELL)
- **Reject**: Hallucinated data, invalid JSON, or nonsensical output

## Performance Targets
- **API latency**: <5 seconds (Claude Sonnet 3.5)
- **Token usage**: ~1000-2000 input tokens, ~500-800 output tokens
- **Cost per analysis**: ~$0.01-0.02 (well within budget for MVP)

## Notes
- Claude API key stored in `.env` as `ANTHROPIC_API_KEY`
- Use Claude 3.5 Sonnet for balance of speed and quality
- Prompt engineering: Iterate based on output quality (update template if consistent issues found)
- Track hallucination rate: If >5% of syntheses contain fabricated data, refine prompt to emphasize "only use provided data"
- Future: Add few-shot examples to prompt for more consistent formatting

## Fallback Strategy
If Claude API unavailable:
1. Generate rule-based summary:
   - If Z-Score < 1.8 → "High risk due to financial distress signals"
   - If sentiment < 40 → "Negative media sentiment detected"
   - Recommendation = weighted average of signals (simple logic)
2. Flag output as "Auto-generated (AI unavailable)" for analyst review
