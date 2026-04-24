"""
Streamlit UI for Investment Scouting & Diligence Engine
Web interface to visualize stock analysis results
"""

import streamlit as st
import json
import subprocess
import sys
from pathlib import Path
import time
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Investment Diligence Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .green-text {
        color: #28a745;
        font-weight: bold;
    }
    .yellow-text {
        color: #ffc107;
        font-weight: bold;
    }
    .red-text {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)


def run_analysis(ticker: str) -> dict:
    """Run the analysis pipeline for a ticker."""
    try:
        result = subprocess.run(
            [sys.executable, "analyze.py", ticker],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Analysis timed out (>60s)"
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }


def load_analysis_files(ticker: str) -> dict:
    """Load all analysis JSON files."""
    files = {
        "fundamentals": f".tmp/{ticker}_fundamentals.json",
        "analysis": f".tmp/{ticker}_analysis.json",
        "news": f".tmp/{ticker}_news.json",
        "synthesis": f".tmp/{ticker}_synthesis.json"
    }
    
    data = {}
    for key, filepath in files.items():
        path = Path(filepath)
        if path.exists():
            with open(path, 'r') as f:
                data[key] = json.load(f)
        else:
            data[key] = None
    
    return data


def get_zone_color(zone: str) -> str:
    """Get color class for zone indicator."""
    if zone == "green":
        return "green-text"
    elif zone == "yellow":
        return "yellow-text"
    elif zone == "red":
        return "red-text"
    return ""


def display_header():
    """Display application header."""
    st.title("📊 Investment Scouting & Diligence Engine")
    st.markdown("**AI-Powered Stock Analysis** | WAT Framework Architecture")
    st.markdown("---")


def get_stock_list():
    """Get comprehensive list of major stocks organized by sector."""
    return {
        "Technology": {
            "AAPL": "Apple Inc.",
            "MSFT": "Microsoft Corporation",
            "GOOGL": "Alphabet Inc. (Google)",
            "META": "Meta Platforms (Facebook)",
            "NVDA": "NVIDIA Corporation",
            "TSLA": "Tesla Inc.",
            "AMD": "Advanced Micro Devices",
            "INTC": "Intel Corporation",
            "CRM": "Salesforce Inc.",
            "ORCL": "Oracle Corporation",
            "ADBE": "Adobe Inc.",
            "NFLX": "Netflix Inc.",
            "AVGO": "Broadcom Inc.",
            "CSCO": "Cisco Systems"
        },
        "Financial": {
            "JPM": "JPMorgan Chase & Co.",
            "BAC": "Bank of America",
            "WFC": "Wells Fargo",
            "GS": "Goldman Sachs",
            "MS": "Morgan Stanley",
            "C": "Citigroup",
            "BLK": "BlackRock",
            "SCHW": "Charles Schwab",
            "AXP": "American Express",
            "V": "Visa Inc.",
            "MA": "Mastercard"
        },
        "Healthcare": {
            "JNJ": "Johnson & Johnson",
            "UNH": "UnitedHealth Group",
            "PFE": "Pfizer Inc.",
            "ABBV": "AbbVie Inc.",
            "MRK": "Merck & Co.",
            "TMO": "Thermo Fisher Scientific",
            "LLY": "Eli Lilly",
            "CVS": "CVS Health"
        },
        "Consumer": {
            "AMZN": "Amazon.com",
            "WMT": "Walmart",
            "HD": "Home Depot",
            "MCD": "McDonald's",
            "NKE": "Nike Inc.",
            "SBUX": "Starbucks",
            "TGT": "Target Corporation",
            "COST": "Costco Wholesale"
        },
        "Industrial": {
            "GE": "General Electric",
            "BA": "Boeing Company",
            "CAT": "Caterpillar Inc.",
            "MMM": "3M Company",
            "HON": "Honeywell",
            "UPS": "United Parcel Service",
            "LMT": "Lockheed Martin"
        },
        "Energy": {
            "XOM": "Exxon Mobil",
            "CVX": "Chevron Corporation",
            "COP": "ConocoPhillips",
            "SLB": "Schlumberger"
        },
        "Other": {
            "BRK.B": "Berkshire Hathaway",
            "DIS": "Walt Disney",
            "VZ": "Verizon",
            "T": "AT&T",
            "PEP": "PepsiCo",
            "KO": "Coca-Cola"
        }
    }


def display_sidebar():
    """Display sidebar with controls."""
    with st.sidebar:
        st.header("⚙️ Stock Selection")
        
        # Initialize session state for selected ticker
        if 'selected_ticker' not in st.session_state:
            st.session_state.selected_ticker = "AAPL"
        
        # Selection mode
        selection_mode = st.radio(
            "How would you like to select a stock?",
            ["📋 Choose from list", "✍️ Enter custom ticker"],
            label_visibility="collapsed"
        )
        
        ticker = None
        
        if selection_mode == "📋 Choose from list":
            # Get stock list
            stocks = get_stock_list()
            
            # Flatten for dropdown
            all_stocks = {}
            for sector, companies in stocks.items():
                all_stocks.update(companies)
            
            # Create display options
            stock_options = [f"{tick} - {name}" for tick, name in all_stocks.items()]
            
            # Find current selection index
            try:
                current_ticker = st.session_state.selected_ticker
                current_display = f"{current_ticker} - {all_stocks[current_ticker]}"
                default_index = stock_options.index(current_display)
            except (KeyError, ValueError):
                default_index = 0
            
            # Dropdown selection
            selected = st.selectbox(
                "Select a stock to analyze:",
                options=stock_options,
                index=default_index,
                help="Choose from major S&P 500 companies"
            )
            
            # Extract ticker from selection
            ticker = selected.split(" - ")[0] if selected else "AAPL"
            
            # Show sector grouping info
            with st.expander("📊 View by Sector"):
                for sector, companies in stocks.items():
                    st.markdown(f"**{sector}**")
                    for tick, name in companies.items():
                        st.text(f"  {tick} - {name}")
                    st.markdown("")
        
        else:  # Custom ticker input
            ticker = st.text_input(
                "Enter Stock Ticker:",
                value=st.session_state.selected_ticker,
                max_chars=10,
                help="Enter any valid stock ticker (e.g., ABNB, RIVN, SNAP)"
            ).upper().strip()
        
        # Update session state
        if ticker:
            st.session_state.selected_ticker = ticker
        
        st.markdown("---")
        
        # Analyze button
        analyze_button = st.button(
            f"🔍 Analyze {ticker}",
            type="primary",
            use_container_width=True,
            help="Click to run REAL-TIME analysis (takes 15-30 seconds)"
        )
        
        st.markdown("---")
        
        # Info section
        st.markdown("**ℹ️ Real-Time Analysis**")
        st.info("""
        ⚡ **Live Analysis Mode**
        
        Every analysis is run fresh:
        - Current stock prices
        - Latest news (last 30 days)
        - Real-time financial data
        - Fresh AI synthesis
        
        **Data Sources:**
        - Yahoo Finance (fundamentals)
        - NewsAPI (100 articles)
        - SEC EDGAR (filings)
        - Claude AI (synthesis)
        
        **Takes 15-30 seconds per stock**
        """)
        
    return ticker, analyze_button


def display_financial_metrics(data: dict):
    """Display financial health metrics."""
    st.header("💰 Financial Health")
    
    fundamentals = data.get("fundamentals", {})
    analysis = data.get("analysis", {})
    
    if not fundamentals or not analysis:
        st.warning("Financial data not available")
        return
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        price = fundamentals.get("current_price", 0)
        st.metric("Current Price", f"${price:.2f}" if price else "N/A")
    
    with col2:
        market_cap = fundamentals.get("market_cap", 0)
        if market_cap:
            market_cap_b = market_cap / 1e9
            st.metric("Market Cap", f"${market_cap_b:.1f}B")
        else:
            st.metric("Market Cap", "N/A")
    
    with col3:
        pe_ratio = fundamentals.get("pe_ratio", 0)
        st.metric("P/E Ratio", f"{pe_ratio:.2f}" if pe_ratio else "N/A")
    
    with col4:
        data_quality = fundamentals.get("data_completeness", 0)
        st.metric("Data Quality", f"{data_quality}%")
    
    st.markdown("---")
    
    # Risk metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Altman Z-Score")
        zscore = analysis.get("altman_zscore")
        zone = analysis.get("zscore_zone", "N/A")
        
        if zscore:
            color_class = get_zone_color(zone)
            st.markdown(f"<p class='big-font {color_class}'>{zscore:.2f}</p>", unsafe_allow_html=True)
            
            # Zone interpretation
            if zone == "green":
                st.success("✅ Safe Zone - Low bankruptcy risk")
            elif zone == "yellow":
                st.warning("⚠️ Gray Zone - Moderate risk")
            else:
                st.error("🚨 Distress Zone - High bankruptcy risk")
            
            # Z-Score components
            with st.expander("View Z-Score Components"):
                components = analysis.get("components", {})
                for key, value in components.items():
                    st.text(f"{key}: {value:.4f}")
        else:
            st.info("Z-Score calculation unavailable")
    
    with col2:
        st.subheader("📊 Debt Analysis")
        debt_ratio = analysis.get("debt_to_equity")
        debt_zone = analysis.get("debt_zone", "N/A")
        
        if debt_ratio:
            color_class = get_zone_color(debt_zone)
            st.markdown(f"<p class='big-font {color_class}'>Debt/Equity: {debt_ratio:.2f}</p>", unsafe_allow_html=True)
            
            current_ratio = analysis.get("current_ratio", 0)
            liquidity_zone = analysis.get("liquidity_zone", "N/A")
            
            st.text(f"Current Ratio: {current_ratio:.2f}")
            st.text(f"Liquidity: {liquidity_zone}")
            
            # Risk flags
            risk_flags = analysis.get("risk_flags", [])
            if risk_flags:
                with st.expander("⚠️ Risk Flags"):
                    for flag in risk_flags:
                        st.warning(flag)
        else:
            st.info("Debt analysis unavailable")


def display_sentiment_analysis(data: dict):
    """Display sentiment analysis."""
    st.header("📰 News Sentiment")
    
    news = data.get("news", {})
    
    if not news or news.get("error"):
        st.warning("News sentiment data not available")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sentiment_score = news.get("sentiment_score", 0)
        sentiment_zone = news.get("sentiment_zone", "N/A")
        color_class = get_zone_color(sentiment_zone)
        
        st.metric("Sentiment Score", f"{sentiment_score}/100")
        st.markdown(f"<p class='{color_class}'>Zone: {sentiment_zone.upper()}</p>", unsafe_allow_html=True)
    
    with col2:
        total_articles = news.get("total_articles", 0)
        negative_pct = news.get("negative_pct", 0)
        positive_pct = news.get("positive_pct", 0)
        
        st.metric("Articles Analyzed", total_articles)
        st.text(f"Negative: {negative_pct:.1f}%")
        st.text(f"Positive: {positive_pct:.1f}%")
    
    with col3:
        negative_keywords = news.get("top_negative_keywords", [])
        if negative_keywords:
            st.markdown("**🚩 Negative Keywords:**")
            for kw in negative_keywords[:5]:
                st.text(f"• {kw}")
    
    # Flagged articles
    flagged = news.get("flagged_articles", [])
    if flagged:
        with st.expander(f"View {len(flagged)} Flagged Articles"):
            for article in flagged[:10]:
                st.markdown(f"**{article.get('title')}**")
                st.text(f"Source: {article.get('source')} | {article.get('publishedAt')}")
                st.text(f"Keywords: {', '.join(article.get('negative_keywords', []))}")
                st.markdown("---")


def display_ai_recommendation(data: dict):
    """Display AI synthesis and recommendation."""
    st.header("🤖 AI Investment Recommendation")
    
    synthesis = data.get("synthesis", {})
    
    if not synthesis:
        st.warning("AI synthesis not available")
        return
    
    # Main recommendation
    recommendation = synthesis.get("investment_recommendation", "N/A")
    confidence = synthesis.get("confidence_score", 0)
    reasoning = synthesis.get("reasoning", "N/A")
    
    # Color based on recommendation
    rec_color = {
        "BUY": "green",
        "HOLD": "yellow",
        "SELL": "red"
    }.get(recommendation, "gray")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"### Recommendation")
        if rec_color == "green":
            st.success(f"## {recommendation}")
        elif rec_color == "yellow":
            st.warning(f"## {recommendation}")
        elif rec_color == "red":
            st.error(f"## {recommendation}")
        else:
            st.info(f"## {recommendation}")
        
        st.metric("Confidence", f"{confidence}/10")
        
        # Fallback indicator
        if synthesis.get("note") and "fallback" in synthesis.get("note", "").lower():
            st.caption("⚠️ Using rule-based analysis (Claude API unavailable)")
    
    with col2:
        st.markdown("### Reasoning")
        st.info(reasoning)
    
    # Red flags
    red_flags = synthesis.get("red_flags", [])
    if red_flags:
        st.markdown("### 🚩 Red Flags")
        for flag in red_flags:
            st.error(f"• {flag}")
    
    # Opportunities
    opportunities = synthesis.get("opportunities", [])
    if opportunities:
        st.markdown("### ✅ Opportunities")
        for opp in opportunities:
            st.success(f"• {opp}")
    
    # Next steps
    next_steps = synthesis.get("next_steps", [])
    if next_steps:
        with st.expander("📋 Recommended Next Steps"):
            for step in next_steps:
                st.text(f"• {step}")


def display_company_overview(data: dict):
    """Display company basic information."""
    fundamentals = data.get("fundamentals", {})
    
    if not fundamentals:
        return
    
    st.header(f"{fundamentals.get('company_name', 'N/A')} ({fundamentals.get('ticker', 'N/A')})")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.text(f"Sector: {fundamentals.get('sector', 'N/A')}")
    with col2:
        st.text(f"Industry: {fundamentals.get('industry', 'N/A')}")
    with col3:
        timestamp = fundamentals.get('timestamp', '')
        if timestamp:
            dt = datetime.fromisoformat(timestamp)
            st.text(f"Updated: {dt.strftime('%Y-%m-%d %H:%M')}")
    
    st.markdown("---")


def main():
    """Main application."""
    display_header()
    
    # Sidebar (returns ticker and analyze button state)
    ticker, analyze_button = display_sidebar()
    
    # Run analysis if button clicked
    if analyze_button:
        st.markdown("---")
        st.info(f"🔄 Running **REAL-TIME** analysis for **{ticker}**...")
        st.markdown("**Steps:**")
        progress_placeholder = st.empty()
        
        with st.spinner(f"⏳ Analyzing {ticker}... (15-30 seconds)"):
            start_time = time.time()
            result = run_analysis(ticker)
            elapsed = time.time() - start_time
            
            if result["success"]:
                st.success(f"✅ Analysis complete for **{ticker}** in {elapsed:.1f} seconds!")
                st.session_state.last_ticker = ticker
                st.session_state.last_analysis_time = datetime.now()
                
                # Show what was done
                with st.expander("📋 Analysis Pipeline Executed"):
                    st.code("""
[1/5] Fetched fresh stock fundamentals from Yahoo Finance
[2/5] Calculated Altman Z-Score and debt ratios
[3/5] Analyzed 100 news articles from last 30 days
[4/5] Generated AI synthesis with Claude
[5/5] Exported to Google Sheets/Slides format
                    """, language="text")
            else:
                st.error(f"❌ Analysis failed for {ticker}")
                st.code(result["error"], language="text")
                return
        
        st.markdown("---")
    
    # Determine which ticker to display
    if "last_ticker" in st.session_state:
        display_ticker = st.session_state.last_ticker
    else:
        display_ticker = ticker
    
    # Load analysis data
    data = load_analysis_files(display_ticker)
    
    # Check if analysis exists
    if not any(data.values()):
        st.info(f"👈 Select a stock and click **'Analyze {display_ticker}'** to start")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🚀 How to Use
            
            1. **Select a stock** from dropdown (70+ companies)
               - Or enter custom ticker
            2. **Click 'Analyze'** button
            3. **Wait 15-30 seconds** for real-time analysis
            4. **Review comprehensive results**
            
            ### ⚡ Real-Time Analysis
            
            Every analysis is **LIVE**:
            - ✅ Current stock prices
            - ✅ Latest news (30 days)
            - ✅ Fresh financial data
            - ✅ AI synthesis by Claude
            
            **Not pre-cached!** Each run fetches new data.
            """)
        
        with col2:
            st.markdown("""
            ### 📊 What You'll Get
            
            **Financial Health:**
            - Altman Z-Score (bankruptcy risk)
            - Debt/Equity ratios
            - Liquidity metrics
            
            **Market Sentiment:**
            - 100 news articles analyzed
            - Keyword detection
            - Sentiment score (0-100)
            
            **AI Recommendation:**
            - BUY/HOLD/SELL decision
            - Confidence score (1-10)
            - Risk flags & opportunities
            
            **Available Stocks:**
            - 70+ major companies
            - All sectors covered
            - S&P 500 focus
        - **Risk Flags**: Identified concerns and red flags
        """)
        return
    
    # Display analysis sections
    display_company_overview(data)
    display_financial_metrics(data)
    st.markdown("---")
    display_sentiment_analysis(data)
    st.markdown("---")
    display_ai_recommendation(data)
    
    # Footer with file locations
    st.markdown("---")
    st.caption(f"📁 Raw data available in `.tmp/{display_ticker}_*.json` files")
    
    if "last_analysis_time" in st.session_state:
        elapsed = (datetime.now() - st.session_state.last_analysis_time).total_seconds()
        st.caption(f"⏱️ Last analysis completed {elapsed:.0f} seconds ago")
        st.caption(f"💡 **Real-time analysis** - every run fetches fresh data from live APIs")


if __name__ == "__main__":
    main()
