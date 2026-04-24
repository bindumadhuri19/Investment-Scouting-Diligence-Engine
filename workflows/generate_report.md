# Workflow: Generate Report

## Objective
Export investment diligence analysis to cloud services (Google Sheets and Google Slides) for stakeholder review.

## Required Inputs
- `.tmp/{ticker}_fundamentals.json`
- `.tmp/{ticker}_analysis.json`
- `.tmp/{ticker}_sentiment.json`
- `.tmp/{ticker}_synthesis.json`
- `.tmp/{ticker}_sec_filings.json` (optional)

## Tools to Execute
1. `tools/export_to_google_sheets.py` - Create investment dashboard spreadsheet
2. `tools/export_to_google_slides.py` - Generate executive summary presentation

## Expected Outputs
- **Google Sheets URL**: Shareable link to investment dashboard
- **Google Slides URL**: Shareable link to executive presentation
- **Permissions**: Both set to "Anyone with link can view" (or restricted to organization domain)

## Google Sheets Structure (4 tabs)

### Tab 1: Company Snapshot
| Field | Value |
|-------|-------|
| Ticker | {ticker} |
| Company Name | {company_name} |
| Sector | {sector} |
| Market Cap | {market_cap} |
| Current Price | {price} |
| 52-Week High/Low | {high} / {low} |
| Volume (Avg) | {avg_volume} |
| P/E Ratio | {pe_ratio} |
| Dividend Yield | {dividend_yield} |
| Analysis Date | {timestamp} |

### Tab 2: Risk Metrics
| Metric | Value | Zone | Flag |
|--------|-------|------|------|
| Altman Z-Score | {zscore} | {zone_color} | {flag_text} |
| Debt/Equity | {ratio} | {zone_color} | {flag_text} |
| OCF/Net Income | {ocf_ratio} | {zone_color} | {flag_text} |
| Current Ratio | {current_ratio} | {zone_color} | {flag_text} |

**Risk Flags**: Bulleted list of all red flags detected

### Tab 3: Sentiment Analysis
| Metric | Value |
|--------|-------|
| Total Articles (30d) | {total_articles} |
| Sentiment Score | {sentiment_score}/100 |
| Negative Articles | {negative_count} ({negative_pct}%) |
| Positive Articles | {positive_count} ({positive_pct}%) |

**Flagged Articles**: Table with columns: Date, Source, Headline, Keywords Detected

### Tab 4: AI Synthesis
| Section | Content |
|---------|---------|
| Risk Summary | {risk_summary} |
| Red Flags | Bulleted list from {red_flags} |
| Opportunities | Bulleted list from {opportunities} |
| Recommendation | {investment_recommendation} |
| Confidence | {confidence_score}/10 |
| Reasoning | {reasoning} |
| Next Steps | Bulleted list from {next_steps} |

**Formatting**:
- Use color coding: Green cells for safe zones, yellow for caution, red for risk
- Bold key metrics (Z-Score, sentiment score, recommendation)
- Hyperlink news articles to source URLs

## Google Slides Structure (5 slides)

### Slide 1: Company Overview
- Title: "{TICKER} Investment Diligence Summary"
- Subtitle: "{Company Name} | {Sector}"
- Bullet points:
  - Market Cap: {market_cap}
  - Current Price: {price} (52-wk range: {low}-{high})
  - P/E Ratio: {pe_ratio}
- Footer: "Analysis Date: {timestamp}"

### Slide 2: Financial Health Scorecard
- Title: "Financial Health Metrics"
- Visual: Traffic light indicators (🟢🟡🔴) for each metric
- Table:
  - Altman Z-Score: {zscore} ({zone})
  - Debt/Equity: {ratio} ({zone})
  - OCF/Net Income: {ocf_ratio} ({zone})
- Key Takeaway: 1-sentence summary of financial health

### Slide 3: Sentiment & News Analysis
- Title: "Market Sentiment (30-Day)"
- Visual: Pie chart (Positive/Neutral/Negative article distribution)
- Key Stats:
  - Sentiment Score: {sentiment_score}/100
  - Flagged Concerns: {top_3_keywords}
- Quote: Most concerning headline (if negative sentiment detected)

### Slide 4: Risk Flags & Concerns
- Title: "Key Risk Flags"
- Bulleted list:
  - {red_flag_1}
  - {red_flag_2}
  - {red_flag_3}
  - ... (all from synthesis)
- Visual: Risk severity indicator (Low/Medium/High)

### Slide 5: Investment Recommendation
- Title: "AI-Powered Recommendation"
- Large text: {BUY / HOLD / SELL}
- Confidence: {confidence_score}/10
- Reasoning: {reasoning} (2-3 sentences)
- Next Steps: Bulleted list of recommended diligence actions

**Formatting**:
- Use corporate color scheme (blues/grays for neutral, red/yellow/green for zones)
- Include disclaimer footer: "AI-assisted analysis. Requires analyst review before action."

## Execution Steps
1. Load all cached JSON files from `.tmp/{ticker}_*`
2. Call `export_to_google_sheets.py`:
   - Authenticate with Google Sheets API (OAuth via credentials.json)
   - Create new spreadsheet: "Investment Diligence - {TICKER} - {DATE}"
   - Populate 4 tabs with structured data
   - Apply formatting (colors, bold, borders)
   - Set sharing permissions
   - Return spreadsheet URL
3. Call `export_to_google_slides.py`:
   - Authenticate with Google Slides API
   - Create new presentation: "{TICKER} Executive Summary - {DATE}"
   - Populate 5 slides from template
   - Apply formatting and visuals
   - Set sharing permissions
   - Return presentation URL
4. Return both URLs to user

## Error Handling
- **Google API authentication failure**: Return error "Google credentials not configured. See setup instructions."
- **API quota exceeded**: Return error "Google API quota exceeded. Try again in 1 hour or upgrade quota."
- **Permission denied**: Check credentials.json has required scopes (sheets, slides)
- **Network timeout**: Retry 2x with 5s delay
- **Partial failure** (e.g., Sheets succeeds but Slides fails): Return Sheets URL + error message for Slides

## Fallback Strategy
If Google APIs unavailable:
1. Export to local files instead:
   - `.tmp/{ticker}_report.xlsx` (Excel file with 4 tabs)
   - `.tmp/{ticker}_summary.pdf` (PDF report using reportlab or similar)
2. Notify user: "Cloud export failed. Local files generated in .tmp/"

## Performance Targets
- **Sheets creation**: <10 seconds
- **Slides creation**: <15 seconds
- **Total export time**: <30 seconds

## Permissions & Security
- **Default sharing**: "Anyone with link can view" (read-only)
- **Optional**: Restrict to organization domain only (configure in export tools)
- **Data retention**: Cloud files persist indefinitely unless manually deleted
- **Local cache**: `.tmp/` files can be deleted after successful cloud export

## Validation
- Verify all tabs/slides created successfully
- Spot-check data accuracy (manual review of 3 cells/slide)
- Test share URLs (open in incognito to verify accessibility)

## Notes
- Google OAuth tokens stored in `token.json` (auto-refreshed, gitignored)
- First-time setup requires interactive OAuth flow (user grants permissions)
- For batch processing, reuse authenticated session (avoid re-auth per ticker)
- Update workflow if Google API changes (e.g., Sheets API v5 released)
- Consider adding export to Google Drive folder for organization (future enhancement)
