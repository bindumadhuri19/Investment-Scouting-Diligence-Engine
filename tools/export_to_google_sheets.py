"""
Export investment analysis to Google Sheets.
Creates 4-tab dashboard with company data, risk metrics, sentiment, and AI synthesis.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime


def export_to_google_sheets(ticker: str, output_dir: str = ".tmp") -> dict:
    """
    Export analysis to Google Sheets.
    
    NOTE: This is a placeholder implementation for MVP.
    Full Google Sheets API integration requires:
    1. OAuth credentials (credentials.json)
    2. google-auth and google-api-python-client packages
    3. Token management (token.json)
    
    Args:
        ticker: Stock symbol
        output_dir: Directory containing analysis JSON files
        
    Returns:
        dict: Status and sheet URL (mock for MVP)
    """
    try:
        # Load all analysis data
        data = load_all_data(ticker, output_dir)
        
        # Check if Google API credentials exist
        credentials_path = Path("credentials.json")
        
        if not credentials_path.exists():
            return create_mock_sheets_export(ticker, data, output_dir)
        
        # Full implementation would go here:
        # - Authenticate with Google Sheets API
        # - Create new spreadsheet
        # - Populate 4 tabs
        # - Apply formatting
        # - Set sharing permissions
        # - Return sheet URL
        
        # For MVP, return mock response
        return create_mock_sheets_export(ticker, data, output_dir)
        
    except Exception as e:
        print(f"✗ Google Sheets export failed: {e}", file=sys.stderr)
        return {
            "error": str(e),
            "ticker": ticker,
            "export_type": "google_sheets",
            "success": False
        }


def load_all_data(ticker: str, output_dir: str) -> dict:
    """Load all analysis JSON files."""
    data = {}
    
    files = {
        "fundamentals": f"{ticker}_fundamentals.json",
        "analysis": f"{ticker}_analysis.json",
        "sentiment": f"{ticker}_news.json",
        "sec": f"{ticker}_sec_filings.json",
        "synthesis": f"{ticker}_synthesis.json"
    }
    
    for key, filename in files.items():
        file_path = Path(output_dir) / filename
        if file_path.exists():
            with open(file_path, 'r') as f:
                data[key] = json.load(f)
        else:
            data[key] = {"warning": f"{filename} not found"}
    
    return data


def create_mock_sheets_export(ticker: str, data: dict, output_dir: str) -> dict:
    """
    Create mock Google Sheets export (fallback for MVP).
    In production, this would create actual Google Sheet.
    For now, export to local Excel-like JSON structure.
    """
    
    # Create structured data for 4 tabs
    sheet_data = {
        "Tab 1: Company Snapshot": create_snapshot_tab(data),
        "Tab 2: Risk Metrics": create_risk_metrics_tab(data),
        "Tab 3: Sentiment Analysis": create_sentiment_tab(data),
        "Tab 4: AI Synthesis": create_synthesis_tab(data)
    }
    
    # Save as JSON (in production, this would be Google Sheets)
    export_path = Path(output_dir) / f"{ticker.upper()}_sheet_export.json"
    with open(export_path, 'w') as f:
        json.dump(sheet_data, f, indent=2)
    
    print(f"[WARN] Google Sheets API not configured")
    print(f"[OK] Mock export saved to {export_path}")
    print(f"   To enable real Google Sheets export:")
    print(f"   1. Set up credentials.json (Google Cloud Console)")
    print(f"   2. Install: pip install google-auth google-api-python-client")
    print(f"   3. Run OAuth flow to get token.json")
    
    return {
        "ticker": ticker.upper(),
        "export_type": "google_sheets_mock",
        "success": True,
        "local_file": str(export_path),
        "sheet_url": f"https://docs.google.com/spreadsheets/d/MOCK-{ticker}-{datetime.now().strftime('%Y%m%d')}",
        "note": "Mock export - Google Sheets API not configured. See README for setup instructions."
    }


def create_snapshot_tab(data: dict) -> dict:
    """Create company snapshot tab data."""
    fundamentals = data.get("fundamentals", {})
    
    return {
        "Ticker": fundamentals.get("ticker", "N/A"),
        "Company Name": fundamentals.get("company_name", "N/A"),
        "Sector": fundamentals.get("sector", "N/A"),
        "Industry": fundamentals.get("industry", "N/A"),
        "Market Cap": f"${fundamentals.get('market_cap', 0):,.0f}",
        "Current Price": f"${fundamentals.get('current_price', 0):.2f}",
        "52-Week High": f"${fundamentals.get('52_week_high', 0):.2f}",
        "52-Week Low": f"${fundamentals.get('52_week_low', 0):.2f}",
        "P/E Ratio": fundamentals.get("pe_ratio", "N/A"),
        "Dividend Yield": f"{fundamentals.get('dividend_yield', 0) * 100:.2f}%" if fundamentals.get('dividend_yield') else "N/A",
        "Analysis Date": fundamentals.get("timestamp", "N/A")
    }


def create_risk_metrics_tab(data: dict) -> dict:
    """Create risk metrics tab data."""
    analysis = data.get("analysis", {})
    
    return {
        "Altman Z-Score": {
            "Value": analysis.get("altman_zscore", "N/A"),
            "Zone": analysis.get("zscore_zone", "N/A"),
            "Interpretation": analysis.get("interpretation", "")
        },
        "Debt/Equity": {
            "Value": analysis.get("debt_to_equity", "N/A"),
            "Zone": analysis.get("debt_zone", "N/A")
        },
        "Current Ratio": {
            "Value": analysis.get("current_ratio", "N/A"),
            "Zone": analysis.get("liquidity_zone", "N/A")
        },
        "OCF/Net Income": {
            "Value": analysis.get("ocf_to_ni", "N/A"),
            "Flag": "Yes" if analysis.get("ocf_flag") else "No"
        },
        "Risk Flags": analysis.get("risk_flags", [])
    }


def create_sentiment_tab(data: dict) -> dict:
    """Create sentiment analysis tab data."""
    sentiment = data.get("sentiment", {})
    
    return {
        "Summary": {
            "Total Articles": sentiment.get("total_articles", 0),
            "Sentiment Score": f"{sentiment.get('sentiment_score', 'N/A')}/100",
            "Sentiment Zone": sentiment.get("sentiment_zone", "N/A"),
            "Negative %": f"{sentiment.get('negative_pct', 0)}%",
            "Positive %": f"{sentiment.get('positive_pct', 0)}%"
        },
        "Top Negative Keywords": sentiment.get("top_negative_keywords", []),
        "Flagged Articles": [
            {
                "Title": article.get("title", ""),
                "Source": article.get("source", ""),
                "Date": article.get("publishedAt", ""),
                "Keywords": ", ".join(article.get("negative_keywords", []))
            }
            for article in sentiment.get("flagged_articles", [])
        ]
    }


def create_synthesis_tab(data: dict) -> dict:
    """Create AI synthesis tab data."""
    synthesis = data.get("synthesis", {})
    
    return {
        "Risk Summary": synthesis.get("risk_summary", "N/A"),
        "Red Flags": synthesis.get("red_flags", []),
        "Opportunities": synthesis.get("opportunities", []),
        "Investment Recommendation": synthesis.get("investment_recommendation", "N/A"),
        "Confidence Score": f"{synthesis.get('confidence_score', 'N/A')}/10",
        "Reasoning": synthesis.get("reasoning", "N/A"),
        "Next Steps": synthesis.get("next_steps", []),
        "Analysis Date": synthesis.get("timestamp", "N/A")
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export_to_google_sheets.py TICKER [output_dir]")
        print("  Reads from: .tmp/TICKER_*.json")
        print("  Exports to: Google Sheets (or mock JSON)")
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    output_dir = sys.argv[2] if len(sys.argv) > 2 else ".tmp"
    
    result = export_to_google_sheets(ticker, output_dir)
    
    if result.get("success"):
        print(f"\n[OK] Export complete!")
        if "sheet_url" in result:
            print(f"  Sheet URL: {result['sheet_url']}")
    else:
        sys.exit(1)
