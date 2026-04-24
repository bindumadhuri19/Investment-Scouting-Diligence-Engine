# Testing Guide

## Quick System Test

Run the comprehensive test suite:

```powershell
python test_system.py
```

This will test all 8 components:
1. ✅ Environment configuration (.env variables)
2. ✅ Python dependencies (yfinance, requests, etc.)
3. ✅ Tool scripts (8 Python files)
4. ✅ Workflow files (6 markdown SOPs)
5. ✅ Data fetching (stock fundamentals, news)
6. ✅ Risk analysis (Z-Score, debt ratios)
7. ✅ AI synthesis (Claude API or fallback)
8. ✅ End-to-end pipeline

---

## Individual Component Tests

### Test 1: Environment Variables
```powershell
Get-Content .env
```
**Expected**: API keys should be configured (ANTHROPIC_API_KEY, NEWSAPI_KEY)

### Test 2: Claude API
```powershell
python test_claude_api.py
```
**Expected**: At least one Claude model should work

**If all models fail with 404**:
- **Cause**: API key may not have access to Claude models
- **Fix Options**:
  1. Check your Anthropic Console: https://console.anthropic.com/
  2. Verify API key tier/permissions
  3. Check model availability: https://docs.anthropic.com/en/docs/models-overview
  4. System will auto-fallback to rule-based analysis (still functional!)

### Test 3: Single Ticker Analysis
```powershell
python analyze.py AAPL
```
**Expected output**:
```
============================================================
Investment Diligence Analysis: AAPL
============================================================

[*] Fetching fresh data...
[1/5] Fetching company data...        ✅
[2/5] Calculating risk metrics...      ✅
[3/5] Analyzing sentiment...           ✅
[4/5] Generating AI synthesis...       ✅
[5/5] Generating reports...            ✅

[OK] Analysis complete in 15-25s

Financial Health:
  Altman Z-Score: X.X (green/yellow/red)
  Debt/Equity: X.XX (zone)

AI Recommendation: BUY/HOLD/SELL
Confidence: X/10
```

### Test 4: Multiple Tickers
```powershell
# Test different company types
python analyze.py TSLA   # High-growth tech
python analyze.py GE     # Mature industrial  
python analyze.py AMD    # Semiconductor
python analyze.py F      # Traditional automotive
```

### Test 5: Verify Output Files
```powershell
Get-ChildItem .tmp\AAPL_*.json
```
**Expected files**:
- `AAPL_fundamentals.json` - Stock data
- `AAPL_analysis.json` - Risk metrics
- `AAPL_news.json` - Sentiment analysis
- `AAPL_synthesis.json` - AI recommendation
- `AAPL_sheet_export.json` - Google Sheets mock
- `AAPL_slides_export.json` - Google Slides mock

### Test 6: Inspect Output Quality
```powershell
Get-Content .tmp\AAPL_synthesis.json | ConvertFrom-Json | Format-List
```
**Check for**:
- `investment_recommendation`: Should be BUY/HOLD/SELL
- `confidence_score`: Should be 1-10
- `reasoning`: Should have meaningful text
- `red_flags`: Should list actual concerns

---

## Common Issues & Solutions

### Issue 1: Claude API Returns 404 (Model Not Found)
**Symptoms**: All Claude models fail with "not_found_error"

**Why it happens**:
- API key doesn't have access to those specific models
- Models deprecated/renamed after April 2026
- Regional/tier restrictions

**Solution**:
1. Check available models at: https://console.anthropic.com/settings/keys
2. Contact Anthropic support for model access
3. **System continues working** - Uses rule-based fallback synthesis

**Verification**:
```powershell
python test_claude_api.py
```

### Issue 2: News Sentiment Fails
**Symptoms**: "[WARN] News sentiment fetch failed"

**Why it happens**:
- NEWSAPI_KEY not set or invalid
- Rate limit exceeded (500 requests/day on free tier)

**Solution**:
1. Get API key: https://newsapi.org/register
2. Add to `.env`: `NEWSAPI_KEY=your_key_here`
3. If rate limited, wait 24 hours or upgrade tier

**Verification**:
```powershell
python tools\fetch_news_sentiment.py AAPL .tmp
```

### Issue 3: SEC Filings Fail
**Symptoms**: "[WARN] SEC filing fetch failed"

**Why it happens**:
- SEC EDGAR API timeout or connectivity issue
- Ticker has no recent filings

**Impact**: Non-critical - other data sources compensate

**Solution**: This is expected in MVP - Phase 5 includes full SEC parser

### Issue 4: Missing Financial Data
**Symptoms**: "Insufficient data for Altman Z-Score calculation"

**Why it happens**:
- yfinance API returned incomplete balance sheet data
- Company is private, delisted, or non-US

**Solution**:
- Try a different ticker (use S&P 500 companies)
- Check if ticker is valid: `python -c "import yfinance as yf; print(yf.Ticker('AAPL').info['longName'])"`

---

## Performance Benchmarks

| Component | Expected Time | Success Rate |
|-----------|---------------|--------------|
| Stock fundamentals | 2-5s | 95% |
| SEC filings | 1-3s | 80% (MVP) |
| News sentiment | 3-8s | 90% |
| Risk metrics | <1s | 98% |
| AI synthesis | 5-10s | 70% (Claude) / 100% (fallback) |
| Report export | <1s | 100% |
| **Full pipeline** | **15-30s** | **95%+** |

---

## Success Criteria

### Minimum Viable (MVP is working):
- ✅ Stock fundamentals fetch successfully
- ✅ Altman Z-Score calculates (non-zero)
- ✅ Investment recommendation generated (BUY/HOLD/SELL)
- ✅ Output files created in `.tmp/`

### Full Production Quality:
- ✅ All above PLUS:
- ✅ Claude AI synthesis working (not fallback)
- ✅ News sentiment >50 articles analyzed
- ✅ SEC filings parsed successfully
- ✅ Google Sheets/Slides real export (not mock)

---

## Debug Mode

Enable detailed logging:

```powershell
# In .env file
DEBUG=true
```

Then run:
```powershell
python analyze.py AAPL
```

You'll see:
- API request/response details
- Model selection process
- Data completeness scores
- Intermediate calculation steps

---

## Test Data Recommendations

### Safe to test (high data quality):
- **AAPL** - Apple Inc. (tech, excellent data)
- **MSFT** - Microsoft (tech, excellent data)
- **JPM** - JPMorgan Chase (finance, excellent data)
- **JNJ** - Johnson & Johnson (healthcare, excellent data)

### Challenging cases (good for edge testing):
- **TSLA** - Tesla (volatile, mixed signals)
- **AMC** - AMC Entertainment (distressed, bankruptcy risk)
- **GME** - GameStop (high volatility, sentiment swings)
- **RIVN** - Rivian (new company, limited history)

### Should fail gracefully:
- **INVALID** - Non-existent ticker
- **PRIVATE** - Private company (no data)
- **DELISTED** - Delisted stock

---

## Automated Testing

For CI/CD or repeated testing:

```powershell
# Run all tests and save report
python test_system.py > test_report.txt 2>&1

# Check exit code
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ All tests passed"
} else {
    Write-Host "❌ Some tests failed - check test_report.txt"
}
```

---

## Getting Help

If tests fail:
1. Check this guide for the specific issue
2. Review error messages in terminal
3. Check `.tmp/` files for detailed error info
4. Enable `DEBUG=true` in `.env`
5. Run `python test_system.py` for comprehensive diagnostics
