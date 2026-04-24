"""
Calculate debt and liquidity ratios.
Includes: Debt/Equity, Current Ratio, OCF/Net Income
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def calculate_debt_ratios(fundamentals: dict) -> dict:
    """
    Calculate debt and liquidity ratios from fundamentals.
    
    Args:
        fundamentals: Dict containing financial metrics
        
    Returns:
        dict: Calculated ratios and risk flags
    """
    try:
        # Extract metrics
        total_debt = fundamentals.get("total_debt", 0)
        total_equity = fundamentals.get("total_equity", 0)
        current_assets = fundamentals.get("current_assets", 0)
        current_liabilities = fundamentals.get("current_liabilities", 0)
        operating_cash_flow = fundamentals.get("operating_cash_flow", 0)
        net_income = fundamentals.get("net_income", 0)
        
        # Calculate ratios
        debt_to_equity = total_debt / total_equity if total_equity > 0 else float('inf')
        current_ratio = current_assets / current_liabilities if current_liabilities > 0 else 0
        ocf_to_ni = operating_cash_flow / net_income if net_income > 0 else 0
        
        # Determine zones
        debt_zone = determine_debt_zone(debt_to_equity)
        liquidity_zone = determine_liquidity_zone(current_ratio)
        ocf_flag = ocf_to_ni < 0.8  # Flag if OCF is significantly below net income
        
        # Generate risk flags
        risk_flags = []
        if debt_zone == "red":
            risk_flags.append("Excessive leverage (Debt/Equity > 2.0)")
        if liquidity_zone == "red":
            risk_flags.append("Liquidity risk (Current Ratio < 1.0)")
        if ocf_flag:
            risk_flags.append("Earnings quality concern (Operating cash flow weak relative to net income)")
        if debt_to_equity == float('inf'):
            risk_flags.append("Negative or zero equity (critical financial distress)")
        
        result = {
            "ticker": fundamentals.get("ticker", "UNKNOWN"),
            "timestamp": datetime.now().isoformat(),
            "debt_to_equity": round(debt_to_equity, 2) if debt_to_equity != float('inf') else "N/A",
            "debt_zone": debt_zone,
            "current_ratio": round(current_ratio, 2),
            "liquidity_zone": liquidity_zone,
            "ocf_to_ni": round(ocf_to_ni, 2),
            "ocf_flag": ocf_flag,
            "risk_flags": risk_flags,
            "data_quality": "complete" if all([total_debt or total_equity, current_assets, net_income]) else "partial"
        }
        
        return result
        
    except Exception as e:
        return {
            "error": f"Ratio calculation failed: {str(e)}",
            "ticker": fundamentals.get("ticker", "UNKNOWN"),
            "timestamp": datetime.now().isoformat()
        }


def determine_debt_zone(debt_to_equity: float) -> str:
    """Determine risk zone based on debt/equity ratio."""
    if debt_to_equity == float('inf'):
        return "red"
    elif debt_to_equity < 1.0:
        return "green"
    elif debt_to_equity <= 2.0:
        return "yellow"
    else:
        return "red"


def determine_liquidity_zone(current_ratio: float) -> str:
    """Determine risk zone based on current ratio."""
    if current_ratio >= 1.5:
        return "green"
    elif current_ratio >= 1.0:
        return "yellow"
    else:
        return "red"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python calculate_debt_ratios.py TICKER [output_dir]")
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
    
    # Calculate ratios
    result = calculate_debt_ratios(fundamentals)
    
    # Load existing analysis or create new
    analysis_path = Path(output_dir) / f"{ticker}_analysis.json"
    if analysis_path.exists():
        with open(analysis_path, 'r') as f:
            analysis = json.load(f)
    else:
        analysis = {"ticker": ticker, "timestamp": datetime.now().isoformat()}
    
    # Merge ratio results
    analysis.update(result)
    
    # Save
    with open(analysis_path, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"[OK] Debt/Equity: {result.get('debt_to_equity', 'N/A')} ({result.get('debt_zone', 'N/A')})")
    print(f"[OK] Current Ratio: {result.get('current_ratio', 'N/A')} ({result.get('liquidity_zone', 'N/A')})")
    print(f"[OK] Analysis saved to {analysis_path}")
    
    if "error" in result:
        sys.exit(1)
