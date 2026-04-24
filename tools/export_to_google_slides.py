"""
Export investment analysis to Google Slides presentation.
Creates 5-slide executive summary deck.
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def export_to_google_slides(ticker: str, output_dir: str = ".tmp") -> dict:
    """
    Export analysis to Google Slides presentation.
    
    NOTE: This is a placeholder implementation for MVP.
    Full Google Slides API integration requires:
    1. OAuth credentials (credentials.json)
    2. google-auth and google-api-python-client packages
    3. Token management (token.json)
    
    Args:
        ticker: Stock symbol
        output_dir: Directory containing analysis JSON files
        
    Returns:
        dict: Status and presentation URL (mock for MVP)
    """
    try:
        # Load all analysis data
        data = load_all_data(ticker, output_dir)
        
        # Check if Google API credentials exist
        credentials_path = Path("credentials.json")
        
        if not credentials_path.exists():
            return create_mock_slides_export(ticker, data, output_dir)
        
        # Full implementation would go here:
        # - Authenticate with Google Slides API
        # - Create new presentation from template
        # - Populate 5 slides with data
        # - Apply formatting and visuals
        # - Set sharing permissions
        # - Return presentation URL
        
        # For MVP, return mock response
        return create_mock_slides_export(ticker, data, output_dir)
        
    except Exception as e:
        print(f"✗ Google Slides export failed: {e}", file=sys.stderr)
        return {
            "error": str(e),
            "ticker": ticker,
            "export_type": "google_slides",
            "success": False
        }


def load_all_data(ticker: str, output_dir: str) -> dict:
    """Load all analysis JSON files."""
    data = {}
    
    files = {
        "fundamentals": f"{ticker}_fundamentals.json",
        "analysis": f"{ticker}_analysis.json",
        "sentiment": f"{ticker}_news.json",
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


def create_mock_slides_export(ticker: str, data: dict, output_dir: str) -> dict:
    """
    Create mock Google Slides export (fallback for MVP).
    In production, this would create actual Google Slides presentation.
    For now, export slide content as structured JSON.
    """
    
    # Create structured content for 5 slides
    slides_content = {
        "Slide 1: Company Overview": create_slide_1(data),
        "Slide 2: Financial Health": create_slide_2(data),
        "Slide 3: Sentiment Analysis": create_slide_3(data),
        "Slide 4: Risk Flags": create_slide_4(data),
        "Slide 5: Recommendation": create_slide_5(data)
    }
    
    # Save as JSON (in production, this would be Google Slides)
    export_path = Path(output_dir) / f"{ticker.upper()}_slides_export.json"
    with open(export_path, 'w') as f:
        json.dump(slides_content, f, indent=2)
    
    print(f"[WARN] Google Slides API not configured")
    print(f"[OK] Mock export saved to {export_path}")
    print(f"   To enable real Google Slides export:")
    print(f"   1. Set up credentials.json (Google Cloud Console)")
    print(f"   2. Install: pip install google-auth google-api-python-client")
    print(f"   3. Run OAuth flow to get token.json")
    
    return {
        "ticker": ticker.upper(),
        "export_type": "google_slides_mock",
        "success": True,
        "local_file": str(export_path),
        "slides_url": f"https://docs.google.com/presentation/d/MOCK-{ticker}-{datetime.now().strftime('%Y%m%d')}",
        "note": "Mock export - Google Slides API not configured. See README for setup instructions."
    }


def create_slide_1(data: dict) -> dict:
    """Slide 1: Company Overview."""
    fundamentals = data.get("fundamentals", {})
    
    return {
        "Title": f"{fundamentals.get('ticker', 'N/A')} Investment Diligence Summary",
        "Subtitle": f"{fundamentals.get('company_name', 'N/A')} | {fundamentals.get('sector', 'N/A')}",
        "Content": [
            f"Market Cap: ${fundamentals.get('market_cap', 0):,.0f}",
            f"Current Price: ${fundamentals.get('current_price', 0):.2f}",
            f"52-Week Range: ${fundamentals.get('52_week_low', 0):.2f} - ${fundamentals.get('52_week_high', 0):.2f}",
            f"P/E Ratio: {fundamentals.get('pe_ratio', 'N/A')}"
        ],
        "Footer": f"Analysis Date: {datetime.now().strftime('%Y-%m-%d')}"
    }


def create_slide_2(data: dict) -> dict:
    """Slide 2: Financial Health Scorecard."""
    analysis = data.get("analysis", {})
    
    zone_emoji = {
        "green": "🟢",
        "yellow": "🟡",
        "red": "🔴",
        "N/A": "⚪"
    }
    
    return {
        "Title": "Financial Health Metrics",
        "Content": {
            "Metrics": [
                {
                    "Metric": "Altman Z-Score",
                    "Value": analysis.get("altman_zscore", "N/A"),
                    "Zone": analysis.get("zscore_zone", "N/A"),
                    "Indicator": zone_emoji.get(analysis.get("zscore_zone", "N/A"), "⚪")
                },
                {
                    "Metric": "Debt/Equity",
                    "Value": analysis.get("debt_to_equity", "N/A"),
                    "Zone": analysis.get("debt_zone", "N/A"),
                    "Indicator": zone_emoji.get(analysis.get("debt_zone", "N/A"), "⚪")
                },
                {
                    "Metric": "Current Ratio",
                    "Value": analysis.get("current_ratio", "N/A"),
                    "Zone": analysis.get("liquidity_zone", "N/A"),
                    "Indicator": zone_emoji.get(analysis.get("liquidity_zone", "N/A"), "⚪")
                }
            ],
            "Key Takeaway": analysis.get("interpretation", "Financial health assessment based on quantitative metrics")
        }
    }


def create_slide_3(data: dict) -> dict:
    """Slide 3: Sentiment & News Analysis."""
    sentiment = data.get("sentiment", {})
    
    return {
        "Title": "Market Sentiment (30-Day)",
        "Content": {
            "Sentiment Score": f"{sentiment.get('sentiment_score', 'N/A')}/100",
            "Distribution": {
                "Negative": f"{sentiment.get('negative_pct', 0)}%",
                "Positive": f"{sentiment.get('positive_pct', 0)}%",
                "Neutral": f"{100 - sentiment.get('negative_pct', 0) - sentiment.get('positive_pct', 0)}%"
            },
            "Top Concerns": sentiment.get("top_negative_keywords", []),
            "Most Concerning Headline": sentiment.get("flagged_articles", [{}])[0].get("title", "No significant concerns") if sentiment.get("flagged_articles") else "No negative headlines"
        }
    }


def create_slide_4(data: dict) -> dict:
    """Slide 4: Risk Flags & Concerns."""
    analysis = data.get("analysis", {})
    synthesis = data.get("synthesis", {})
    
    all_red_flags = list(set(
        analysis.get("risk_flags", []) + 
        synthesis.get("red_flags", [])
    ))
    
    return {
        "Title": "Key Risk Flags",
        "Content": {
            "Red Flags": all_red_flags if all_red_flags else ["No significant risks identified"],
            "Risk Severity": determine_risk_severity(all_red_flags)
        }
    }


def create_slide_5(data: dict) -> dict:
    """Slide 5: Investment Recommendation."""
    synthesis = data.get("synthesis", {})
    
    recommendation = synthesis.get("investment_recommendation", "HOLD")
    confidence = synthesis.get("confidence_score", "N/A")
    
    return {
        "Title": "AI-Powered Recommendation",
        "Content": {
            "Recommendation": recommendation,
            "Confidence": f"{confidence}/10",
            "Reasoning": synthesis.get("reasoning", "Analysis in progress"),
            "Next Steps": synthesis.get("next_steps", ["Manual review recommended"])
        },
        "Disclaimer": "AI-assisted analysis. Requires analyst review before investment action."
    }


def determine_risk_severity(red_flags: list) -> str:
    """Determine overall risk severity based on number of red flags."""
    count = len(red_flags)
    if count == 0:
        return "Low"
    elif count <= 2:
        return "Medium"
    else:
        return "High"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export_to_google_slides.py TICKER [output_dir]")
        print("  Reads from: .tmp/TICKER_*.json")
        print("  Exports to: Google Slides (or mock JSON)")
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    output_dir = sys.argv[2] if len(sys.argv) > 2 else ".tmp"
    
    result = export_to_google_slides(ticker, output_dir)
    
    if result.get("success"):
        print(f"\n[OK] Export complete!")
        if "slides_url" in result:
            print(f"  Slides URL: {result['slides_url']}")
    else:
        sys.exit(1)
