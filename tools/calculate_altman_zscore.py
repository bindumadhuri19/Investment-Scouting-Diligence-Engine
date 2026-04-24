"""
Calculate Altman Z-Score for bankruptcy prediction.
Formula: Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5

Where:
X1 = Working Capital / Total Assets
X2 = Retained Earnings / Total Assets
X3 = EBIT / Total Assets
X4 = Market Value of Equity / Total Liabilities
X5 = Sales (Revenue) / Total Assets
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def calculate_altman_zscore(fundamentals: dict) -> dict:
    """
    Calculate Altman Z-Score from fundamentals data.
    
    Args:
        fundamentals: Dict containing financial metrics
        
    Returns:
        dict: Z-Score and interpretation
    """
    try:
        # Extract required metrics
        working_capital = fundamentals.get("working_capital", 0)
        total_assets = fundamentals.get("total_assets", 0)
        retained_earnings = calculate_retained_earnings(fundamentals)
        ebit = fundamentals.get("ebit", 0)
        market_cap = fundamentals.get("market_cap", 0)
        total_liabilities = fundamentals.get("total_liabilities", 0)
        revenue = fundamentals.get("revenue", 0)
        
        # Check for missing/zero denominators
        if total_assets == 0:
            return create_insufficient_data_response(fundamentals.get("ticker", "UNKNOWN"))
        
        # Calculate components
        x1 = working_capital / total_assets if total_assets != 0 else 0
        x2 = retained_earnings / total_assets if total_assets != 0 else 0
        x3 = ebit / total_assets if total_assets != 0 else 0
        x4 = market_cap / total_liabilities if total_liabilities != 0 else 0
        x5 = revenue / total_assets if total_assets != 0 else 0
        
        # Calculate Z-Score
        z_score = (1.2 * x1) + (1.4 * x2) + (3.3 * x3) + (0.6 * x4) + (1.0 * x5)
        
        # Determine zone
        if z_score > 3.0:
            zone = "green"
            interpretation = "Safe zone - Low bankruptcy risk"
        elif z_score >= 1.8:
            zone = "yellow"
            interpretation = "Gray zone - Moderate risk, caution advised"
        else:
            zone = "red"
            interpretation = "Distress zone - High bankruptcy risk"
        
        result = {
            "ticker": fundamentals.get("ticker", "UNKNOWN"),
            "timestamp": datetime.now().isoformat(),
            "altman_zscore": round(z_score, 2),
            "zscore_zone": zone,
            "interpretation": interpretation,
            "components": {
                "x1_working_capital_ratio": round(x1, 4),
                "x2_retained_earnings_ratio": round(x2, 4),
                "x3_ebit_ratio": round(x3, 4),
                "x4_market_value_ratio": round(x4, 4),
                "x5_asset_turnover": round(x5, 4)
            },
            "data_quality": "complete" if all([working_capital, total_assets, ebit, market_cap, revenue]) else "partial"
        }
        
        return result
        
    except Exception as e:
        return {
            "error": f"Z-Score calculation failed: {str(e)}",
            "ticker": fundamentals.get("ticker", "UNKNOWN"),
            "timestamp": datetime.now().isoformat(),
            "altman_zscore": None,
            "zscore_zone": "N/A"
        }


def calculate_retained_earnings(fundamentals: dict) -> float:
    """
    Estimate retained earnings from available data.
    If not directly available, approximate as: Total Equity - Paid-in Capital
    """
    # yfinance doesn't always provide retained earnings directly
    # Use approximation: Retained Earnings ≈ Total Equity - (Market Cap - Net Income)
    # Or simply use net_income as proxy for recent earnings retention
    
    total_equity = fundamentals.get("total_equity", 0)
    net_income = fundamentals.get("net_income", 0)
    
    # Simple approximation (not perfectly accurate but reasonable for MVP)
    if total_equity > 0:
        return total_equity * 0.6  # Assume ~60% of equity is retained earnings
    elif net_income > 0:
        return net_income * 3  # Approximate 3 years of earnings
    else:
        return 0


def create_insufficient_data_response(ticker: str) -> dict:
    """Create response when data is insufficient for Z-Score calculation."""
    return {
        "error": "Insufficient data for Altman Z-Score calculation",
        "ticker": ticker,
        "timestamp": datetime.now().isoformat(),
        "altman_zscore": None,
        "zscore_zone": "N/A",
        "note": "Total assets is zero or missing critical financial data"
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python calculate_altman_zscore.py TICKER [output_dir]")
        print("  Reads from: .tmp/TICKER_fundamentals.json")
        print("  Appends to: .tmp/TICKER_analysis.json")
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    output_dir = sys.argv[2] if len(sys.argv) > 2 else ".tmp"
    
    # Load fundamentals
    fundamentals_path = Path(output_dir) / f"{ticker}_fundamentals.json"
    
    if not fundamentals_path.exists():
        print(f"[ERROR] Fundamentals file not found: {fundamentals_path}", file=sys.stderr)
        sys.exit(1)
    
    with open(fundamentals_path, 'r') as f:
        fundamentals = json.load(f)
    
    # Calculate Z-Score
    result = calculate_altman_zscore(fundamentals)
    
    # Load existing analysis if present, or create new
    analysis_path = Path(output_dir) / f"{ticker}_analysis.json"
    if analysis_path.exists():
        with open(analysis_path, 'r') as f:
            analysis = json.load(f)
    else:
        analysis = {"ticker": ticker, "timestamp": datetime.now().isoformat()}
    
    # Merge Z-Score results
    analysis.update(result)
    
    # Save
    with open(analysis_path, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"[OK] Z-Score: {result.get('altman_zscore', 'N/A')} ({result.get('zscore_zone', 'N/A')})")
    print(f"[OK] Analysis saved to {analysis_path}")
    
    if "error" in result:
        sys.exit(1)
