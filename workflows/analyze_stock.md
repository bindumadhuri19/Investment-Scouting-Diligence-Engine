# Workflow: Analyze Stock

## Objective
Generate comprehensive investment due diligence report for a given stock ticker, aggregating financial data, sentiment analysis, and AI-powered synthesis.

## Required Inputs
- **Stock ticker** (string): Valid US stock symbol (e.g., "AAPL", "TSLA", "MSFT")

## Tools to Execute (in sequence)
1. `workflows/fetch_company_data.md` - Aggregate data from multiple APIs
2. `workflows/calculate_risk_metrics.md` - Compute financial health scores
3. `workflows/analyze_sentiment.md` - Analyze news sentiment and insider activity
4. `workflows/synthesize_analysis.md` - Generate AI-powered risk synthesis
5. `workflows/generate_report.md` - Export to Google Sheets and Slides

## Expected Outputs
- **Google Sheets URL**: Investment dashboard with 4 tabs (snapshot, metrics, news, synthesis)
- **Google Slides URL**: Executive summary presentation (5 slides)
- **Cache files** in `.tmp/`: Intermediate JSON files (disposable, 1-hour TTL)

## Execution Steps
1. Validate ticker symbol (uppercase, alphanumeric only)
2. Check cache: If `.tmp/{ticker}_*` files exist and <1 hour old, skip API calls
3. Execute sub-workflows in sequence (each handles its own error recovery)
4. Aggregate results from all `.tmp/{ticker}_*.json` files
5. Export to cloud services (Google Sheets + Slides)
6. Return URLs to user

## Error Handling
- **Invalid ticker**: Return error message "Ticker '{ticker}' not found or invalid"
- **API failures**: Retry 3x with exponential backoff (1s, 2s, 4s). If all fail, use cached data if available
- **Cache miss + API failure**: Return error "Unable to fetch data for {ticker}. Please try again later."
- **Partial data**: Flag missing sections in final report (e.g., "SEC filing data unavailable")
- **Google API failures**: Fall back to local JSON export in `.tmp/`, notify user

## Edge Cases
- **Delisted stock**: Will fail at yfinance fetch → graceful error message
- **Pre-revenue company**: Altman Z-Score may be invalid (division by zero) → flag as "N/A"
- **Non-US ticker**: May lack SEC filings → skip SEC workflow, flag in report
- **Low news volume**: <5 articles in 30 days → sentiment score marked "Insufficient data"
- **API rate limits**: Exponential backoff + caching mitigates; worst case uses stale data

## Success Criteria
- All 5 sub-workflows complete successfully
- Google Sheets contains 4 populated tabs
- Google Slides contains 5 populated slides
- Analysis completes in <30 seconds (with cache) or <60 seconds (fresh)

## Human Review Required
- Analyst must review Claude synthesis before sharing with external clients
- Verify red flags accuracy (target: <15% false positive rate)

## Notes
- Update this workflow when discovering new edge cases (e.g., "API X changed rate limits")
- Cache expiration set to 1 hour (market data changes intraday, but analysis timescale is days)
- For batch analysis (multiple tickers), call this workflow in loop with 2s delay between calls
