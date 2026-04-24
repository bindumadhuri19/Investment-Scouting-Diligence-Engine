# Deployment Information

## Live System Access & Setup Instructions

---

## 🌐 Live Deployment

### Streamlit Cloud (Primary)

**URL:** https://investment-scouting-diligence-engine-jybimqhynh27qytati59.streamlit.app/

**Status:** ✅ Live and operational

**Features:**
- Real-time stock analysis
- 70+ pre-loaded tickers
- Interactive dashboard
- No authentication required
- Auto-deploys from GitHub

**How to Use:**
1. Open the URL above
2. Select a stock from dropdown or enter custom ticker
3. Click "Analyze [TICKER]"
4. Wait 15-30 seconds for real-time analysis
5. Explore results (financial metrics, Z-score, sentiment, AI recommendation)

---

## 📁 GitHub Repository

**URL:** https://github.com/bindumadhuri19/Investment-Scouting-Diligence-Engine

**Repository Structure:**
```
Investment-Scouting-Diligence-Engine/
├── analyze.py              # Main orchestrator
├── app.py                  # Streamlit UI
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
├── workflows/              # Markdown SOPs
│   ├── analyze_stock.md
│   ├── fetch_data.md
│   ├── assess_financial_risk.md
│   ├── analyze_sentiment.md
│   ├── synthesize_with_ai.md
│   └── export_reports.md
├── tools/                  # Python execution scripts
│   ├── fetch_stock_fundamentals.py
│   ├── fetch_sec_filings.py
│   ├── fetch_news_sentiment.py
│   ├── calculate_financial_risk.py
│   ├── synthesize_with_claude.py
│   ├── export_to_sheets.py
│   ├── export_to_slides.py
│   └── validate_data.py
├── .tmp/                   # Cache directory (gitignored)
└── [Documentation files]
```

**Clone Command:**
```bash
git clone https://github.com/bindumadhuri19/Investment-Scouting-Diligence-Engine.git
```

---

## 💻 Local Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Internet connection (for API calls)

### Step-by-Step Setup

**1. Clone the repository:**
```bash
git clone https://github.com/bindumadhuri19/Investment-Scouting-Diligence-Engine.git
cd Investment-Scouting-Diligence-Engine
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Configure environment variables:**
```bash
# Copy the template
cp .env.example .env

# Edit .env with your API keys
notepad .env  # Windows
nano .env     # Linux/Mac
```

**Required API Keys:**
```env
ANTHROPIC_API_KEY=your_claude_api_key_here
NEWSAPI_KEY=your_newsapi_key_here
CACHE_TTL=3600
DEBUG=false
```

**Where to get API keys:**
- **Anthropic Claude:** https://console.anthropic.com/
- **NewsAPI:** https://newsapi.org/register (free tier: 500 requests/day)

**4. Run the application:**

**Option A: Streamlit UI**
```bash
streamlit run app.py
```
Opens at: http://localhost:8501

**Option B: Command-line**
```bash
python analyze.py AAPL
```
Analyzes Apple stock and saves results to `.tmp/`

---

## 🔑 API Requirements

### Required APIs

**1. Anthropic Claude API**
- **Cost:** Pay-per-use (starts at ~$0.01 per analysis)
- **Free tier:** No free tier, but minimal cost
- **Sign up:** https://console.anthropic.com/
- **Usage:** AI synthesis and recommendations

**2. NewsAPI**
- **Cost:** Free tier available
- **Limits:** 500 requests/day (plenty for testing)
- **Sign up:** https://newsapi.org/register
- **Usage:** Sentiment analysis from news articles

### Optional APIs (Not Required)

**3. Yahoo Finance (yfinance)**
- **Cost:** Free
- **Limits:** None (rate-limited but generous)
- **Sign up:** Not required
- **Usage:** Stock fundamentals and prices

**4. SEC EDGAR**
- **Cost:** Free
- **Limits:** Rate-limited (be respectful)
- **Sign up:** Not required
- **Usage:** Company filings and legal info

---

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Easiest)

**Already deployed!** Access at the URL above.

**To deploy your own:**
1. Fork the GitHub repository
2. Go to https://share.streamlit.io/
3. Click "New app"
4. Connect your GitHub account
5. Select your forked repo
6. Add secrets (API keys) in Settings → Secrets
7. Deploy!

**Secrets format for Streamlit Cloud:**
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
NEWSAPI_KEY = "abc123..."
```

### Option 2: Heroku

**Steps:**
1. Create Heroku account
2. Install Heroku CLI
3. Create `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT
   ```
4. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku config:set ANTHROPIC_API_KEY=your_key
   heroku config:set NEWSAPI_KEY=your_key
   ```

### Option 3: Docker

**Create `Dockerfile`:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

**Build and run:**
```bash
docker build -t investment-engine .
docker run -p 8501:8501 --env-file .env investment-engine
```

### Option 4: AWS EC2

**Steps:**
1. Launch EC2 instance (Ubuntu 22.04)
2. SSH into instance
3. Install Python and dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip
   git clone [repo-url]
   cd Investment-Scouting-Diligence-Engine
   pip install -r requirements.txt
   ```
4. Configure environment variables
5. Run with tmux or systemd:
   ```bash
   tmux new -s streamlit
   streamlit run app.py --server.port 80
   ```

### Option 5: Google Cloud Run

**Steps:**
1. Create `cloudbuild.yaml`:
   ```yaml
   steps:
   - name: 'gcr.io/cloud-builders/docker'
     args: ['build', '-t', 'gcr.io/$PROJECT_ID/investment-engine', '.']
   images:
   - 'gcr.io/$PROJECT_ID/investment-engine'
   ```
2. Deploy:
   ```bash
   gcloud builds submit --config cloudbuild.yaml
   gcloud run deploy investment-engine --image gcr.io/$PROJECT_ID/investment-engine
   ```

---

## 🧪 Testing

### Run System Tests

```bash
python test_system.py
```

**Expected output:**
```
Testing Environment Configuration... PASSED
Testing Stock Fundamentals Fetch... PASSED
Testing Financial Risk Calculation... PASSED
Testing News Sentiment Analysis... PASSED
Testing SEC Filing Fetch... PASSED
Testing Claude Synthesis... PASSED
Testing End-to-End Pipeline... PASSED
Testing Cache Mechanism... PASSED

All tests passed! ✅
```

### Run Individual Tools

**Test stock fundamentals:**
```bash
python tools/fetch_stock_fundamentals.py AAPL .tmp
cat .tmp/AAPL_fundamentals.json
```

**Test risk calculation:**
```bash
python tools/calculate_financial_risk.py AAPL .tmp
cat .tmp/AAPL_analysis.json
```

**Test full analysis:**
```bash
python analyze.py MSFT
```

---

## 📊 Available Stocks

**Pre-loaded tickers (70+):**

**Technology:**
AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA, AMD, INTC, CRM

**Finance:**
JPM, BAC, WFC, GS, MS, C, BLK, AXP, V, MA

**Healthcare:**
JNJ, UNH, PFE, ABBV, TMO, ABT, MRK, LLY, AMGN, CVS

**Consumer:**
WMT, PG, KO, PEP, COST, NKE, MCD, SBUX, HD, TGT

**Energy:**
XOM, CVX, COP, SLB, EOG, MPC, PSX, VLO, OXY, HAL

**And more!** See `STOCKS_AVAILABLE.md` for full list.

**Custom tickers:** You can also enter any valid US stock ticker.

---

## 🔧 Configuration

### Environment Variables

**Required:**
- `ANTHROPIC_API_KEY` - Claude API key
- `NEWSAPI_KEY` - NewsAPI key

**Optional:**
- `CACHE_TTL` - Cache duration in seconds (default: 3600)
- `DEBUG` - Enable debug logging (default: false)
- `ALPHA_VANTAGE_KEY` - Fallback stock data (optional)
- `FINNHUB_API_KEY` - Additional market data (optional)

### Cache Settings

**Location:** `.tmp/` directory

**TTL:** 1 hour (3600 seconds) by default

**Clear cache:**
```bash
# Windows
Remove-Item .tmp\* -Force

# Linux/Mac
rm -rf .tmp/*
```

---

## 🐛 Troubleshooting

### Common Issues

**1. "Module not found" error**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**2. "API key not found" error**
```bash
# Solution: Check .env file
cat .env  # Verify keys are set
```

**3. "Rate limit exceeded" (NewsAPI)**
```bash
# Solution: Wait or use different API key
# Free tier: 500 requests/day
```

**4. Streamlit app won't start**
```bash
# Solution: Check if port 8501 is free
netstat -ano | findstr :8501  # Windows
lsof -i :8501                 # Linux/Mac

# Use different port
streamlit run app.py --server.port 8502
```

**5. "No data available" for stock**
```bash
# Possible causes:
# - Invalid ticker symbol
# - Stock delisted
# - API timeout

# Try with known-good ticker
python analyze.py AAPL
```

---

## 📞 Support & Contact

**GitHub Issues:** https://github.com/bindumadhuri19/Investment-Scouting-Diligence-Engine/issues

**Email:** binduchalasani19@gmail.com

**Documentation:** See repository README.md

---

## ✅ Verification Checklist

Before evaluating, verify:

- [ ] Live Streamlit app is accessible
- [ ] GitHub repository is public
- [ ] Can clone repository locally
- [ ] Dependencies install successfully
- [ ] Tests pass with `python test_system.py`
- [ ] Can analyze at least one stock
- [ ] Results display correctly
- [ ] Documentation is clear and complete

---

## 🎯 Quick Evaluation Guide

**For Reviewers:**

**5-Minute Quick Test:**
1. Visit live Streamlit app
2. Select "GOOGL" from dropdown
3. Click "Analyze GOOGL"
4. Review results (should show metrics, Z-score, recommendation)

**15-Minute Deep Dive:**
1. Clone GitHub repository
2. Run `python test_system.py`
3. Try 2-3 different stocks
4. Review code structure in `analyze.py` and `tools/`

**30-Minute Full Review:**
1. Read `TECHNICAL_ARCHITECTURE.md`
2. Review `REQUIREMENTS_CHECKLIST.md`
3. Run local installation
4. Analyze multiple stocks
5. Review all documentation

---

**System is live, tested, and ready for evaluation!** 🚀
