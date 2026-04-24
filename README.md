# Investment Scouting & Diligence Engine

AI-powered investment due diligence platform built with the **WAT Framework** (Workflows, Agents, Tools).

Compresses research timelines from **days to minutes** by aggregating financial data, news sentiment, and AI-powered risk analysis into actionable investment reports.

---

## Features

✅ **Automated Data Aggregation**
- Stock fundamentals (yfinance)
- SEC filings (EDGAR API)
- News sentiment (NewsAPI)

✅ **Quantitative Risk Metrics**
- Altman Z-Score (bankruptcy prediction)
- Debt ratios and liquidity analysis
- Earnings quality indicators

✅ **AI-Powered Synthesis**
- Claude API generates investment diligence summary
- Identifies red flags, opportunities, and recommendations
- BUY/HOLD/SELL recommendations with confidence scores

✅ **Cloud Deliverables**
- Google Sheets dashboard (4 tabs: snapshot, metrics, sentiment, synthesis)
- Google Slides executive summary (5 slides)

---

## Quick Start

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API keys in .env
#    ANTHROPIC_API_KEY=your_key
#    NEWSAPI_KEY=your_key

# 3. Run analysis
python analyze.py AAPL
```

See [SETUP.md](SETUP.md) for detailed setup instructions.

---

## WAT Framework Architecture

### Layer 1: Workflows (Markdown SOPs)
6 workflow files in `workflows/` define:
- Objectives, required inputs, tools to execute, expected outputs
- Error handling, edge cases, success criteria

| Workflow | Purpose |
|----------|---------|
| `analyze_stock.md` | Master orchestration workflow |
| `fetch_company_data.md` | Data aggregation from APIs |
| `calculate_risk_metrics.md` | Financial health scoring |
| `analyze_sentiment.md` | News sentiment analysis |
| `synthesize_analysis.md` | AI-powered synthesis |
| `generate_report.md` | Export to cloud services |

### Layer 2: Agent (analyze.py)
Intelligent coordination:
- Reads workflow SOPs
- Executes tools in correct sequence
- Handles failures (retry, fallback, cache)
- Updates workflows when learning from errors

### Layer 3: Tools (Python Scripts)
8 deterministic scripts in `tools/`:
- `fetch_stock_fundamentals.py` - yfinance integration
- `fetch_sec_filings.py` - SEC EDGAR data
- `fetch_news_sentiment.py` - News sentiment scoring
- `calculate_altman_zscore.py` - Bankruptcy prediction
- `calculate_debt_ratios.py` - Leverage analysis
- `synthesize_with_claude.py` - AI synthesis
- `export_to_google_sheets.py` - Cloud export
- `export_to_google_slides.py` - Executive deck

---

## Directory Structure

```
Project_Ajaia/
├── workflows/          # 6 Markdown SOPs (instructions)
├── tools/              # 8 Python scripts (execution)
├── .tmp/               # Cached results (disposable, 1-hour TTL)
├── analyze.py          # Main orchestrator
├── requirements.txt    # Dependencies
├── .env                # API keys (gitignored)
├── SETUP.md            # Setup instructions
├── CLAUDE.md           # WAT framework documentation
└── README.md           # This file
```

---

## Example Output

```
============================================================
Investment Diligence Analysis: AAPL
============================================================

[1/5] Fetching company data...
✓ Fundamentals saved
✓ SEC filings saved
✓ News sentiment saved

[2/5] Calculating risk metrics...
✓ Z-Score: 5.23 (green) - Safe zone
✓ Debt/Equity: 1.57 (yellow) - Moderate

[3/5] Analyzing sentiment...
✓ Sentiment Score: 72/100 (positive)

[4/5] Generating AI synthesis...
✓ Recommendation: BUY
✓ Confidence: 8/10

[5/5] Generating reports...
✓ Google Sheets: .tmp/AAPL_sheet_export.json
✓ Google Slides: .tmp/AAPL_slides_export.json

============================================================
✓ Analysis complete in 12.3s
============================================================

📊 ANALYSIS SUMMARY
Altman Z-Score: 5.23 (green)
Recommendation: BUY (8/10 confidence)
Reasoning: Strong financial health, positive sentiment...
```

---

## Assignment Deliverables

This project was built for the **AI Delivery Lead Technical Challenge**.

### Delivered Components

1. ✅ **Solution Architecture** - WAT framework (3 layers)
2. ✅ **Delivery Plan** - See [/memories/session/plan.md](/memories/session/plan.md)
3. ✅ **Working Prototype** - Full system operational
4. ✅ **Dependencies & Risks** - Documented in workflows
5. ✅ **Launch Readiness Criteria** - In plan document
6. ✅ **Executive Status Update** - Template in plan
7. ✅ **AI Workflow Note** - See below

---

## AI Usage Note

### AI Tools Used

**Claude (Anthropic)**: 
- Used for: Investment risk synthesis, red flag detection, BUY/HOLD/SELL recommendations
- What it accelerated: Analysis quality, natural language reasoning about complex financial data
- What I controlled: Prompt engineering, data validation, fallback logic, confidence scoring

**GitHub Copilot**:
- Used for: Code generation for Python tools, boilerplate reduction
- What it accelerated: Tool script scaffolding, API integration patterns, error handling
- What I controlled: Architecture decisions, workflow design, integration logic, testing

### Decision Making

- **Architecture**: WAT framework choice (not AI-generated)
- **Data sources**: yfinance, NewsAPI, SEC EDGAR selection (manual research)
- **Risk thresholds**: Altman Z-Score zones, debt ratios (domain expertise + research)
- **Error handling**: Retry logic, fallback strategies (designed manually)
- **Workflow sequence**: Tool orchestration order (optimized for reliability)

### Key Tradeoffs

✅ **Chose**: Claude Sonnet 3.5 (balance of speed + quality)  
❌ **Over**: GPT-4 (cost), open-source LLMs (reliability)

✅ **Chose**: Simple keyword sentiment (MVP speed)  
❌ **Over**: ML-based FinBERT (4-hour time constraint)

✅ **Chose**: Mock Google export (MVP feasibility)  
❌ **Over**: Full Google API integration (time vs. value)

---

## Next Steps for Production

1. **Google API Integration** - Replace mock export with real Google Sheets/Slides API
2. **Litigation Detection** - Add PACER scraping or data vendor partnership
3. **Database Layer** - Replace `.tmp/` JSON with PostgreSQL for historical tracking
4. **Web UI** - Streamlit dashboard for interactive analysis
5. **Batch Processing** - Multi-ticker portfolio analysis
6. **ML Sentiment** - Upgrade from keyword-based to FinBERT model

---

## Key Principles

- **Separation of Concerns**: Workflows define intent, agents coordinate, tools execute
- **Reliability**: Deterministic code for execution, AI for reasoning
- **Self-Improvement**: Workflows evolve based on discovered edge cases
- **Cloud First**: Deliverables to Google Sheets/Slides, local files disposable

See [CLAUDE.md](CLAUDE.md) for full WAT framework documentation.

---

## License

Built for Ajaia AI Delivery Lead Technical Challenge (2026)
