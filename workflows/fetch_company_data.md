# Workflow: Fetch Company Data

## Objective
Aggregate company data from multiple public sources in parallel to minimize latency.

## Required Inputs
- **Stock ticker** (string): Valid US stock symbol

## Tools to Execute (in parallel)
1. `tools/fetch_stock_fundamentals.py` - yfinance API
2. `tools/fetch_sec_filings.py` - SEC EDGAR API
3. `tools/fetch_news_sentiment.py` - NewsAPI

## Expected Outputs
- `.tmp/{ticker}_fundamentals.json` - Price, volume, market cap, ratios, cash flow
- `.tmp/{ticker}_sec_filings.json` - Latest 10-K summary, filing date
- `.tmp/{ticker}_news.json` - 30-day article list with sentiment keywords

## Execution Steps
1. Check cache: If all 3 output files exist and timestamp <1 hour, skip fetch
2. Run all 3 tools in parallel (use threading or async)
3. Each tool writes to its own `.tmp/` file independently
4. Wait for all 3 to complete (or timeout after 15 seconds)
5. Verify all 3 files created successfully

## Error Handling Per Tool

### fetch_stock_fundamentals.py
- **yfinance API failure**: Retry 3x with 1s, 2s, 4s delays
- **Ticker not found**: Return error JSON `{"error": "Ticker not found", "ticker": "{ticker}"}`
- **Timeout (>5s)**: Cancel and use cached data if available
- **Fallback**: If yfinance fails, try Alpha Vantage API (if configured)

### fetch_sec_filings.py
- **No 10-K found**: Return JSON `{"error": "No SEC filings found", "ticker": "{ticker}"}`
- **Parsing failure**: Return minimal data `{"filing_date": null, "summary": "Unable to parse"}`
- **SEC API down**: Skip gracefully, flag in final report as "Data unavailable"

### fetch_news_sentiment.py
- **NewsAPI rate limit (500/day exceeded)**: Use cached data, warn user
- **<5 articles found**: Return data but flag `{"warning": "Low article count"}`
- **API key missing**: Return error `{"error": "NewsAPI key not configured"}`

## Cache Strategy
- **Cache location**: `.tmp/{ticker}_*.json`
- **TTL**: 1 hour (3600 seconds)
- **Cache invalidation**: Check file modification time; if >1hr, re-fetch
- **Partial cache**: If only 1-2 files cached, still fetch missing ones

## Validation
After all fetches complete:
1. Verify each JSON file is valid (parseable)
2. Check required fields exist (e.g., `ticker`, `timestamp`)
3. Log any warnings (missing data, API errors)

## Performance Targets
- **With cache**: <500ms (just file reads)
- **Fresh fetch**: <10 seconds (parallel API calls)
- **Worst case (retries)**: <20 seconds

## Notes
- **API key management**: Read from `.env` file (NEWSAPI_KEY, ALPHA_VANTAGE_KEY optional)
- **Rate limit tracking**: Log API call counts to avoid hitting daily limits
- **yfinance unofficial**: No official rate limit, but throttle to 1 req/sec to be safe
- **Update workflow** when discovering API changes (e.g., "NewsAPI changed endpoint")
