# Setup Instructions

## Quick Start (5 minutes)

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit `.env` file and add your API keys:

```env
# REQUIRED (free trials available)
ANTHROPIC_API_KEY=your_key_here  # Get at: https://console.anthropic.com/
NEWSAPI_KEY=your_key_here        # Get at: https://newsapi.org/register
```

### 3. Run Analysis

```powershell
python analyze.py AAPL
```

That's it! The system will:
- Fetch stock data (yfinance)
- Analyze financial health (Altman Z-Score, debt ratios)
- Fetch news sentiment (NewsAPI)
- Generate AI synthesis (Claude)
- Export results to `.tmp/` folder

---

## Detailed Setup

### API Keys (Required)

#### Anthropic Claude API
1. Go to https://console.anthropic.com/
2. Sign up for free ($5 trial credit)
3. Create API key
4. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

**Cost**: ~$0.01-0.02 per company analysis

#### NewsAPI
1. Go to https://newsapi.org/register
2. Sign up for free tier (500 requests/day)
3. Get API key
4. Add to `.env`: `NEWSAPI_KEY=...`

**Cost**: Free (500/day limit)

### Optional: Google Sheets/Slides Export

For real cloud export (not just mock JSON), you need Google Cloud credentials:

1. **Create Google Cloud Project**
   - Go to https://console.cloud.google.com/
   - Create new project
   - Enable Google Sheets API and Google Slides API

2. **Create OAuth Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Create "OAuth 2.0 Client ID" (Desktop application)
   - Download JSON as `credentials.json` (place in project root)

3. **First Run Authentication**
   - Run `python analyze.py AAPL`
   - Browser will open for OAuth consent
   - Grant permissions
   - `token.json` will be created automatically

4. **Update Export Tools** (not implemented in MVP)
   - Modify `tools/export_to_google_sheets.py` to use real Google Sheets API
   - Modify `tools/export_to_google_slides.py` to use real Google Slides API

**Note**: MVP uses mock export (JSON files in `.tmp/`). Production implementation would integrate full Google APIs.

---

## Project Structure

```
Project_Ajaia/
├── workflows/                  # 6 workflow SOPs (markdown)
│   ├── analyze_stock.md
│   ├── fetch_company_data.md
│   ├── calculate_risk_metrics.md
│   ├── analyze_sentiment.md
│   ├── synthesize_analysis.md
│   └── generate_report.md
│
├── tools/                      # 8 Python tool scripts
│   ├── fetch_stock_fundamentals.py
│   ├── fetch_sec_filings.py
│   ├── fetch_news_sentiment.py
│   ├── calculate_altman_zscore.py
│   ├── calculate_debt_ratios.py
│   ├── synthesize_with_claude.py
│   ├── export_to_google_sheets.py
│   └── export_to_google_slides.py
│
├── .tmp/                       # Cached results (disposable)
│   └── TICKER_*.json
│
├── analyze.py                  # Main orchestrator
├── requirements.txt            # Python dependencies
├── .env                        # API keys (gitignored)
├── .gitignore
├── README.md
├── SETUP.md                    # This file
└── CLAUDE.md                   # WAT framework documentation
```

---

## Testing

### Test with Sample Ticker

```powershell
python analyze.py AAPL
```

Expected output:
```
============================================================
Investment Diligence Analysis: AAPL
============================================================

[1/5] Fetching company data...
✓ Fundamentals saved to .tmp/AAPL_fundamentals.json
✓ SEC filings saved to .tmp/AAPL_sec_filings.json
✓ News sentiment saved to .tmp/AAPL_news.json

[2/5] Calculating risk metrics...
✓ Z-Score: 5.23 (green)
✓ Debt/Equity: 1.57 (yellow)

[3/5] Analyzing sentiment...
✓ Sentiment data available

[4/5] Generating AI synthesis...
✓ Synthesis saved to .tmp/AAPL_synthesis.json
✓ Recommendation: BUY
✓ Confidence: 8/10

[5/5] Generating reports...
⚠ Google Sheets API not configured
✓ Mock export saved to .tmp/AAPL_sheet_export.json
⚠ Google Slides API not configured
✓ Mock export saved to .tmp/AAPL_slides_export.json

============================================================
✓ Analysis complete in 12.3s
============================================================

📊 ANALYSIS SUMMARY
------------------------------------------------------------
Ticker: AAPL

Financial Health:
  Altman Z-Score: 5.23 (green)
  Debt/Equity: 1.57 (yellow)

AI Recommendation: BUY
Confidence: 8/10

Reasoning: Strong financial health with Z-Score in safe zone...

🚩 Red Flags:
  • None detected

📁 Results saved to .tmp/AAPL_*.json
📊 Google Sheets: .tmp/AAPL_sheet_export.json
📊 Google Slides: .tmp/AAPL_slides_export.json
```

### Test Additional Tickers

```powershell
python analyze.py TSLA
python analyze.py GE
python analyze.py AMD
```

---

## Troubleshooting

### Error: "NewsAPI key not configured"

**Solution**: Add `NEWSAPI_KEY` to `.env` file

### Error: "Claude API quota exceeded"

**Solution**: 
1. Check API usage at https://console.anthropic.com/
2. Add more credits or wait for monthly reset
3. Fallback: System will use rule-based synthesis instead

### Error: "Ticker not found"

**Solution**: Verify ticker symbol is correct (use Yahoo Finance symbol)

### Slow performance (>60s per analysis)

**Solution**:
1. Check internet connection
2. Reduce `days` parameter in news fetch (default 30)
3. Use cached data (re-run same ticker within 1 hour)

---

## Next Steps

### For Production Deployment

1. **Implement Real Google API Integration**
   - Complete `export_to_google_sheets.py` with Google Sheets API
   - Complete `export_to_google_slides.py` with Google Slides API

2. **Add Database Layer**
   - Replace `.tmp/` JSON with PostgreSQL
   - Store historical analysis for trend tracking

3. **Scale to Batch Processing**
   - Add `batch_analyze.py` for multi-ticker processing
   - Implement async/parallel processing

4. **Enhanced Features**
   - Litigation detection (PACER scraping or data vendor)
   - Multi-company comparison dashboard
   - Email alerts for watchlist

5. **UI Layer**
   - Web dashboard (Streamlit, FastAPI + React, or similar)
   - User authentication and portfolios

---

## WAT Framework Compliance

This project follows the WAT (Workflows, Agents, Tools) framework:

- ✅ **Workflows**: 6 markdown SOPs define objectives, inputs, tools, outputs, edge cases
- ✅ **Agent**: `analyze.py` orchestrates workflows, handles errors, caches results
- ✅ **Tools**: 8 deterministic Python scripts for API calls and calculations
- ✅ **Cloud Deliverables**: Google Sheets/Slides export (mock in MVP, real in production)
- ✅ **Disposable Intermediates**: All `.tmp/` files can be regenerated

See [CLAUDE.md](CLAUDE.md) for full WAT framework documentation.
