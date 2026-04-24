# Web UI Guide

## 🚀 Quick Start

Launch the web interface:

```powershell
streamlit run app.py
```

The UI will open automatically in your browser at `http://localhost:8501`

---

## 📱 UI Features

### **1. Interactive Dashboard**
- Clean, professional interface
- Real-time analysis execution
- Visual metrics and charts
- Color-coded risk indicators

### **2. Analysis Sections**

**📊 Company Overview**
- Company name, sector, industry
- Last update timestamp

**💰 Financial Health**
- Current price, market cap, P/E ratio
- Altman Z-Score with zone indicator (green/yellow/red)
- Debt/Equity ratio analysis
- Liquidity metrics
- Risk flags

**📰 News Sentiment**
- Sentiment score (0-100)
- Articles analyzed count
- Positive/negative breakdown
- Flagged articles with negative keywords

**🤖 AI Recommendation**
- BUY/HOLD/SELL recommendation
- Confidence score (1-10)
- Detailed reasoning
- Red flags and opportunities
- Next steps

### **3. Sidebar Controls**

**Ticker Input**
- Enter any stock ticker (e.g., AAPL, MSFT, TSLA)
- Quick-select sample tickers

**Sample Tickers**
- AAPL - Apple Inc.
- MSFT - Microsoft
- TSLA - Tesla
- GE - General Electric
- JPM - JPMorgan Chase

**About Section**
- Tool overview
- Data sources
- Analysis components

---

## 🎨 Visual Indicators

### **Color Coding**

| Color | Meaning | Example |
|-------|---------|---------|
| 🟢 Green | Safe/Good | Z-Score > 3.0 |
| 🟡 Yellow | Moderate/Caution | Z-Score 1.8-3.0 |
| 🔴 Red | Risk/Concern | Z-Score < 1.8 |

### **Icons**

| Icon | Purpose |
|------|---------|
| 📊 | Financial metrics |
| 📰 | News and sentiment |
| 🤖 | AI recommendation |
| 🚩 | Red flags/warnings |
| ✅ | Opportunities/positives |
| ⚠️ | Caution/moderate risk |

---

## 💡 How to Use

### **Basic Workflow**

1. **Launch UI**: `streamlit run app.py`
2. **Enter Ticker**: Type stock symbol (e.g., "AAPL") in sidebar
3. **Run Analysis**: Click "🔍 Run Analysis" button
4. **Wait**: Analysis takes 15-30 seconds
5. **Review Results**: Scroll through sections
6. **Try Another**: Enter new ticker and repeat

### **Example Session**

```powershell
# Step 1: Launch UI
streamlit run app.py

# Browser opens to http://localhost:8501

# Step 2: In the UI sidebar
# - Enter ticker: AAPL
# - Click "Run Analysis"
# - Wait ~20 seconds

# Step 3: Review results
# - Financial Health: Z-Score 9.6 (green)
# - Debt Analysis: 1.03 D/E (yellow)
# - Sentiment: 52/100 (neutral)
# - Recommendation: HOLD (5/10 confidence)

# Step 4: Try another stock
# - Click "TSLA - Tesla" quick-select button
# - Analysis auto-runs
# - Compare results
```

---

## 🔧 UI Configuration

### **Port Configuration**

Default: `http://localhost:8501`

Change port:
```powershell
streamlit run app.py --server.port 8080
```

### **Theme Customization**

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### **Browser Auto-Open**

Disable auto-open:
```powershell
streamlit run app.py --server.headless true
```

---

## 📊 Understanding the Dashboard

### **Financial Health Section**

**Metrics Row**
- **Current Price**: Real-time stock price
- **Market Cap**: Company valuation (in billions)
- **P/E Ratio**: Price-to-earnings multiple
- **Data Quality**: % of required data available

**Altman Z-Score Panel**
- **Score**: Numerical bankruptcy prediction (higher = safer)
- **Zone**: Color-coded risk level
- **Components**: Expandable detail view with 5 formula components

**Debt Analysis Panel**
- **Debt/Equity**: Leverage ratio
- **Current Ratio**: Liquidity measure
- **Risk Flags**: Expandable list of concerns

### **News Sentiment Section**

**Summary Metrics**
- **Sentiment Score**: 0-100 scale (0=very negative, 100=very positive)
- **Zone**: Color indicator (green/yellow/red)
- **Articles Analyzed**: Total count from last 30 days
- **Positive/Negative %**: Article breakdown

**Flagged Articles**
- Expandable list of articles with negative keywords
- Shows title, source, date, and detected keywords

### **AI Recommendation Section**

**Main Recommendation**
- Large, color-coded BUY/HOLD/SELL decision
- Confidence score (1-10 scale)
- Fallback indicator if Claude API unavailable

**Reasoning**
- Natural language explanation of recommendation
- Factors considered in decision

**Red Flags**
- List of identified risks and concerns
- Expandable for full details

**Opportunities**
- Positive factors (when applicable)

**Next Steps**
- Actionable recommendations for further due diligence

---

## 🐛 Troubleshooting

### **Issue: UI won't start**

**Error**: `streamlit: command not found`

**Solution**:
```powershell
pip install streamlit
streamlit run app.py
```

### **Issue: Analysis stuck/timeout**

**Symptoms**: Spinner runs >60 seconds

**Solutions**:
1. Check internet connection (API calls required)
2. Verify API keys in `.env` file
3. Check if ticker is valid
4. Restart UI and try again

### **Issue: Data not displaying**

**Symptoms**: "Analysis not available" message

**Solutions**:
1. Click "Run Analysis" button first
2. Wait for analysis to complete
3. Check `.tmp/` folder for JSON files
4. Try running `python analyze.py AAPL` in terminal first

### **Issue: Port already in use**

**Error**: `Address already in use`

**Solution**:
```powershell
# Use different port
streamlit run app.py --server.port 8502
```

Or kill existing process:
```powershell
# Find process using port 8501
netstat -ano | findstr :8501

# Kill process (replace PID)
taskkill /PID <PID> /F
```

---

## 🎯 Pro Tips

### **1. Batch Analysis**

Analyze multiple stocks quickly:
- Run analysis for AAPL
- While reviewing, click TSLA quick-select
- Automatic re-analysis
- Compare side-by-side (use browser tabs)

### **2. Data Refresh**

Force fresh data (ignore cache):
```powershell
# Delete cache before analysis
Remove-Item .tmp\AAPL_*.json
# Then run analysis in UI
```

### **3. Export Results**

Save analysis results:
- Screenshots: Built-in browser screenshot
- Raw data: JSON files in `.tmp/` folder
- Reports: Mock Google Sheets/Slides exports available

### **4. Keyboard Shortcuts**

Streamlit built-in shortcuts:
- `R` - Rerun the app
- `C` - Clear cache
- `?` - Show keyboard shortcuts

---

## 📈 Advanced Features

### **Custom Ticker Lists**

Edit `app.py` to add your watchlist:

```python
sample_tickers = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft",
    "YOUR_TICKER": "Your Company Name",
    # Add more...
}
```

### **Data Export Button**

Add to `app.py`:

```python
# In display_ai_recommendation() function
if st.button("📥 Download Full Report"):
    report_data = {
        "ticker": ticker,
        "timestamp": datetime.now().isoformat(),
        "analysis": data
    }
    st.download_button(
        label="Download JSON",
        data=json.dumps(report_data, indent=2),
        file_name=f"{ticker}_analysis_report.json",
        mime="application/json"
    )
```

### **Historical Tracking**

Track analysis over time (requires database):
- Add SQLite database
- Store each analysis run
- Show trend charts
- Compare historical Z-Scores

---

## 🚀 Deployment (Optional)

### **Streamlit Cloud (Free)**

1. Push code to GitHub
2. Sign up at https://streamlit.io/cloud
3. Connect repository
4. Deploy app
5. Share public URL

### **Local Network Access**

Access from other devices on your network:

```powershell
streamlit run app.py --server.address 0.0.0.0
```

Then access from other devices:
`http://YOUR_IP:8501`

---

## 📚 Additional Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **Component Gallery**: https://streamlit.io/components
- **Deployment Guide**: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app

---

## 🎓 UI Architecture

```
app.py (Streamlit UI)
    ↓
    Calls analyze.py (subprocess)
    ↓
    Reads .tmp/*.json files
    ↓
    Displays results in browser
```

**Benefits**:
- ✅ No code duplication (reuses analyze.py)
- ✅ Same analysis pipeline as CLI
- ✅ Visual presentation of complex data
- ✅ Interactive exploration
- ✅ User-friendly for non-technical users
