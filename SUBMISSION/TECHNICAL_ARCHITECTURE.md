# Technical Architecture

## Investment Scouting & Diligence Engine

**A production-ready AI system for automated investment research**

---

## Architecture Overview

The system is built on the **WAT Framework** - a three-layer architecture that separates concerns for reliability, maintainability, and scalability.

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│              Streamlit Web Dashboard (app.py)               │
│         Interactive UI with real-time visualizations        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                      │
│              Main Agent (analyze.py)                        │
│       Reads workflows, executes tools, manages state        │
└─────────────────────────────────────────────────────────────┘
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│   WORKFLOWS (SOPs)      │   │   TOOLS (Execution)     │
│   Markdown instructions │   │   Python scripts        │
│   - analyze_stock.md    │   │   - fetch_*.py          │
│   - assess_risk.md      │   │   - calculate_*.py      │
│   - synthesize.md       │   │   - synthesize_*.py     │
└─────────────────────────┘   └─────────────────────────┘
                                          │
                                          ▼
                              ┌─────────────────────────┐
                              │   EXTERNAL APIs         │
                              │   - Yahoo Finance       │
                              │   - NewsAPI             │
                              │   - SEC EDGAR           │
                              │   - Claude API          │
                              └─────────────────────────┘
```

---

## Layer 1: Workflows (The Instructions)

**Location:** `workflows/` directory  
**Format:** Markdown files  
**Purpose:** Define what to do, not how to do it

### Key Workflows:

1. **analyze_stock.md** - Main orchestration workflow
   - Defines 5-step analysis pipeline
   - Specifies data sources and tools
   - Describes output format

2. **fetch_data.md** - Data gathering workflow
   - Parallel fetching strategy
   - Fallback mechanisms
   - Data validation rules

3. **assess_financial_risk.md** - Risk calculation workflow
   - Altman Z-Score components
   - Debt ratio formulas
   - Liquidity metrics

4. **analyze_sentiment.md** - Sentiment analysis workflow
   - News source selection
   - Keyword weighting
   - Scoring algorithm

5. **synthesize_with_ai.md** - AI synthesis workflow
   - Prompt engineering strategy
   - Context assembly
   - Output validation

6. **export_reports.md** - Export workflow
   - Format specifications
   - Delivery mechanisms
   - Error handling

**Why Markdown?** Human-readable, version-controllable, easy to update without touching code.

---

## Layer 2: Agent (The Orchestrator)

**File:** `analyze.py`  
**Lines:** ~450  
**Purpose:** Intelligent coordination and execution

### Key Functions:

```python
def main(ticker: str):
    """
    Main orchestration following workflows/analyze_stock.md
    """
    # 1. Check cache (avoid redundant API calls)
    if check_cache(ticker):
        use_cache = True
    
    # 2. Fetch company data (parallel execution)
    if not use_cache:
        fetch_company_data(ticker)
    
    # 3. Calculate risk metrics
    calculate_risk_metrics(ticker)
    
    # 4. Analyze sentiment
    analyze_sentiment(ticker)
    
    # 5. Generate AI synthesis
    synthesize_analysis(ticker)
    
    # 6. Export reports
    export_reports(ticker)
    
    # 7. Display summary
    display_summary(ticker)
```

### Responsibilities:
- Read and interpret workflows
- Execute tools in correct sequence
- Handle errors gracefully with fallbacks
- Manage state and caching
- Provide progress feedback
- Validate outputs

### Cache Strategy:
- 1-hour TTL (configurable via `.env`)
- Stored in `.tmp/` directory as JSON
- Automatic invalidation
- Reduces API calls and improves speed

---

## Layer 3: Tools (The Executors)

**Location:** `tools/` directory  
**Type:** Python scripts  
**Purpose:** Deterministic execution of specific tasks

### Tool Inventory:

1. **fetch_stock_fundamentals.py**
   - Connects to Yahoo Finance
   - Extracts 70+ metrics
   - Returns standardized JSON
   - Handles missing data gracefully

2. **fetch_sec_filings.py**
   - Queries SEC EDGAR database
   - Parses filing metadata
   - Validates dates
   - Returns filing information

3. **fetch_news_sentiment.py**
   - Calls NewsAPI
   - Fetches last 30 days of articles
   - Applies keyword scoring
   - Returns sentiment summary

4. **calculate_financial_risk.py**
   - Implements Altman Z-Score formula
   - Calculates debt ratios
   - Assesses liquidity
   - Flags risk zones

5. **synthesize_with_claude.py**
   - Assembles context from all data
   - Calls Claude API with prompt
   - Parses AI response
   - Validates recommendation format
   - Falls back to rule-based logic if API fails

6. **export_to_sheets.py**
   - Formats data for Google Sheets
   - (MVP: Mock export, production would use real API)

7. **export_to_slides.py**
   - Formats data for Google Slides
   - (MVP: Mock export, production would use real API)

8. **validate_data.py**
   - Data quality checks
   - Completeness scoring
   - Error detection

### Tool Design Principles:
- ✅ Single responsibility
- ✅ Idempotent (same input = same output)
- ✅ Fail gracefully with clear errors
- ✅ Return structured JSON
- ✅ Self-contained (no cross-dependencies)

---

## Data Flow

### End-to-End Pipeline:

```
1. USER INPUT
   ↓ (stock ticker)
   
2. CACHE CHECK
   ↓ (if cached < 1 hour, skip to step 6)
   
3. DATA FETCHING (Parallel)
   ├─ Yahoo Finance → fundamentals.json
   ├─ SEC EDGAR → sec_filings.json
   └─ NewsAPI → news.json
   ↓
   
4. RISK CALCULATION
   ├─ Altman Z-Score
   ├─ Debt Analysis
   └─ Liquidity Metrics
   ↓ → analysis.json
   
5. AI SYNTHESIS
   ├─ Assemble all data
   ├─ Build Claude prompt
   ├─ Get recommendation
   └─ Validate output
   ↓ → synthesis.json
   
6. EXPORT & DISPLAY
   ├─ Save to JSON files
   ├─ (Mock) Export to Sheets/Slides
   └─ Display in UI
   ↓
   
7. USER OUTPUT
   Dashboard with metrics, recommendations, insights
```

### Data Formats:

All intermediate data stored as JSON in `.tmp/` directory:
- `{TICKER}_fundamentals.json` - Stock metrics
- `{TICKER}_analysis.json` - Risk calculations
- `{TICKER}_news.json` - Sentiment data
- `{TICKER}_sec_filings.json` - Legal filings
- `{TICKER}_synthesis.json` - AI recommendations
- `{TICKER}_sheet_export.json` - Sheets format (mock)
- `{TICKER}_slides_export.json` - Slides format (mock)

---

## Technology Stack

### Core Technologies:
- **Python 3.x** - Primary language
- **Streamlit** - Web UI framework (simple, fast, interactive)
- **Claude Sonnet 4.5** - AI synthesis and recommendations
- **yfinance** - Stock data (free, no API key required)
- **NewsAPI** - Sentiment data (500 requests/day free)
- **SEC EDGAR** - Legal filings (free, public API)

### Key Libraries:
```
anthropic>=0.25.0       # Claude API client
yfinance>=0.2.28        # Yahoo Finance integration
requests>=2.31.0        # HTTP requests
streamlit>=1.28.0       # Web UI
python-dotenv>=1.0.0    # Environment management
```

### Why These Choices?

**Streamlit** - Fastest way to build interactive dashboards without frontend complexity  
**Claude** - Best-in-class for reasoning and synthesis tasks  
**yfinance** - Most reliable free stock data API  
**NewsAPI** - Good free tier for sentiment analysis  
**SEC EDGAR** - Official source for legal filings  

All choices prioritize:
1. ✅ Reliability
2. ✅ Free/low-cost APIs
3. ✅ Easy deployment
4. ✅ Production-ready

---

## Risk Detection Implementation

### 1. Financial Risk (Altman Z-Score)

**Formula:**
```
Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5

Where:
X1 = Working Capital / Total Assets
X2 = Retained Earnings / Total Assets
X3 = EBIT / Total Assets
X4 = Market Value of Equity / Total Liabilities
X5 = Sales / Total Assets
```

**Risk Zones:**
- Z > 3.0: Green (Safe)
- 1.8 < Z < 3.0: Yellow (Gray zone)
- Z < 1.8: Red (Distress)

**Additional Metrics:**
- Debt-to-Equity ratio
- Current ratio (liquidity)
- OCF/Net Income ratio (cash quality)

### 2. Sentiment Risk

**Method:** Keyword-based scoring with 100+ recent articles

**Keywords:**
- Negative (25): lawsuit, fraud, investigation, scandal, layoff, bankruptcy, etc.
- Positive (12): growth, innovation, profit, expansion, acquisition, etc.

**Scoring:**
```
Sentiment Score = 50 + (positive_count * 2) - (negative_count * 2)
Bounded to [0, 100]
```

**Zones:**
- Score > 60: Green (Positive)
- 40 < Score < 60: Yellow (Neutral)
- Score < 40: Red (Negative)

### 3. Legal Risk

**Data Source:** SEC EDGAR filings

**Flags:**
- Recent enforcement actions
- Material legal proceedings
- Regulatory investigations
- Unusual filing patterns

**Implementation:** MVP extracts metadata only; production would parse full 10-K documents.

---

## AI Integration Strategy

### Claude's Role:

**Not used for:**
- ❌ Calculations (use formulas)
- ❌ Data fetching (use APIs)
- ❌ Deterministic logic (use Python)

**Used for:**
- ✅ Synthesizing diverse data
- ✅ Contextual reasoning
- ✅ Natural language recommendations
- ✅ Identifying patterns humans might miss

### Prompt Engineering:

```python
prompt = f"""
You are an expert investment analyst. Analyze this company:

FINANCIAL HEALTH:
{json.dumps(fundamentals, indent=2)}

RISK METRICS:
{json.dumps(analysis, indent=2)}

MARKET SENTIMENT:
{json.dumps(sentiment, indent=2)}

LEGAL STATUS:
{json.dumps(sec_filings, indent=2)}

Provide:
1. Risk summary (2-3 sentences)
2. Red flags (specific concerns)
3. Opportunities (growth potential)
4. Investment recommendation (BUY/HOLD/SELL)
5. Confidence score (1-10)
6. Reasoning (why this recommendation)
"""
```

### Fallback Strategy:

If Claude API fails, use rule-based logic:
- Z-Score < 1.8 → SELL
- Z-Score > 3.0 + Sentiment > 50 → BUY
- Otherwise → HOLD

This ensures the system always produces results, even without AI.

---

## Deployment Architecture

### Local Development:
```
Project/
├── analyze.py          # Main orchestrator
├── app.py              # Streamlit UI
├── workflows/          # Markdown SOPs
├── tools/              # Python scripts
├── .env                # API keys (not committed)
├── requirements.txt    # Dependencies
└── .tmp/               # Cache directory
```

### Streamlit Cloud Production:
- Automatic deployment from GitHub
- Secrets management for API keys
- HTTPS by default
- Auto-scaling
- Zero-downtime updates

### Environment Variables:
```
ANTHROPIC_API_KEY=<claude-key>
NEWSAPI_KEY=<news-key>
CACHE_TTL=3600
DEBUG=false
```

---

## Scalability Considerations

### Current Capacity:
- Single stock analysis: 15-30 seconds
- Concurrent users: Limited by Streamlit Cloud free tier
- API rate limits: 500 NewsAPI calls/day, unlimited yfinance

### For Production Scale:

**Phase 2 Enhancements:**
- Background job queue for analysis
- Redis caching instead of file-based
- Load balancer for multiple Streamlit instances
- Database for historical data

**Phase 3 (Enterprise):**
- Kubernetes deployment
- Microservices architecture
- Real-time WebSocket updates
- Multi-region support

---

## Testing Strategy

**Current Testing:**
- 8 system tests in `test_system.py`
- End-to-end pipeline validation
- API integration checks
- Error handling verification

**Production Testing Would Include:**
- Unit tests for each tool
- Integration tests for workflows
- Load testing for scale
- Security testing for APIs

---

## Security Considerations

**Current Implementation:**
- API keys in `.env` (not committed)
- Streamlit Cloud secrets for production
- No user authentication (demo only)
- Public data only (no PII)

**Production Requirements:**
- User authentication and authorization
- API rate limiting
- Input sanitization
- Audit logging
- Compliance with financial regulations

---

## Why This Architecture Works

**1. Separation of Concerns**
- AI handles reasoning
- Scripts handle execution
- Workflows handle coordination

**2. Maintainability**
- Each component has single responsibility
- Easy to update workflows without code changes
- Tools can be enhanced independently

**3. Reliability**
- Fallback mechanisms at every layer
- Deterministic tools for calculations
- Graceful error handling

**4. Scalability**
- Stateless design
- Parallelizable data fetching
- Cacheable results

**5. Transparency**
- Clear data flow
- Auditable decision-making
- Explainable recommendations

---

This architecture demonstrates production-grade design principles applied to an AI system built under time constraints.
