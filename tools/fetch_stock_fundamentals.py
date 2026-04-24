"""
Fetch stock fundamentals using yfinance API.
Output: JSON file with price, volume, market cap, ratios, and cash flow data.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
import yfinance as yf


def get_balance_sheet_value(balance_sheet, field_name: str):
    """
    Extract value from balance sheet dataframe.
    Returns the most recent value (first column) if available.
    """
    if balance_sheet is None or balance_sheet.empty:
        return None
    
    try:
        if field_name in balance_sheet.index:
            # Get most recent value (first column)
            value = balance_sheet.loc[field_name].iloc[0]
            return float(value) if value is not None and value > 0 else None
    except:
        pass
    
    return None


def fetch_stock_fundamentals(ticker: str, output_dir: str = ".tmp") -> dict:
    """
    Fetch comprehensive stock fundamentals for a given ticker.
    
    Args:
        ticker: Stock symbol (e.g., "AAPL")
        output_dir: Directory to save JSON output
        
    Returns:
        dict: Fundamentals data
    """
    try:
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Fetch stock data
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get historical data for price trends
        hist = stock.history(period="1y")
        
        # Get balance sheet data (more reliable than info dict)
        try:
            balance_sheet = stock.quarterly_balance_sheet
        except:
            balance_sheet = None
        
        if hist.empty or not info:
            return {
                "error": "Ticker not found or no data available",
                "ticker": ticker,
                "timestamp": datetime.now().isoformat()
            }
        
        # Extract key fundamentals
        fundamentals = {
            "ticker": ticker.upper(),
            "timestamp": datetime.now().isoformat(),
            "company_name": info.get("longName", info.get("shortName", "N/A")),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            
            # Price data
            "current_price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
            "market_cap": info.get("marketCap", 0),
            "enterprise_value": info.get("enterpriseValue", 0),
            
            # Valuation ratios
            "pe_ratio": info.get("trailingPE", info.get("forwardPE", 0)),
            "pb_ratio": info.get("priceToBook", 0),
            "ps_ratio": info.get("priceToSalesTrailing12Months", 0),
            
            # Price ranges
            "52_week_high": info.get("fiftyTwoWeekHigh", 0),
            "52_week_low": info.get("fiftyTwoWeekLow", 0),
            
            # Volume
            "avg_volume": info.get("averageVolume", 0),
            "volume": info.get("volume", 0),
            
            # Financial health metrics (for Altman Z-Score)
            # Try to get from balance sheet first, fallback to info
            "total_assets": get_balance_sheet_value(balance_sheet, "Total Assets") or info.get("totalAssets", 0),
            "total_liabilities": get_balance_sheet_value(balance_sheet, "Total Liabilities Net Minority Interest") or info.get("totalDebt", 0),
            "total_equity": get_balance_sheet_value(balance_sheet, "Stockholders Equity") or info.get("totalStockholderEquity", 0),
            "current_assets": get_balance_sheet_value(balance_sheet, "Current Assets") or info.get("totalCurrentAssets", 0),
            "current_liabilities": get_balance_sheet_value(balance_sheet, "Current Liabilities") or info.get("totalCurrentLiabilities", 0),
            "working_capital": (get_balance_sheet_value(balance_sheet, "Current Assets") or info.get("totalCurrentAssets", 0)) - (get_balance_sheet_value(balance_sheet, "Current Liabilities") or info.get("totalCurrentLiabilities", 0)),
            
            # Income statement
            "revenue": info.get("totalRevenue", 0),
            "ebit": info.get("ebit", 0),
            "net_income": info.get("netIncomeToCommon", 0),
            "gross_profit": info.get("grossProfits", 0),
            
            # Cash flow
            "operating_cash_flow": info.get("operatingCashflow", 0),
            "free_cash_flow": info.get("freeCashflow", 0),
            
            # Debt metrics
            "total_debt": info.get("totalDebt", 0),
            "long_term_debt": info.get("longTermDebt", 0),
            "debt_to_equity": info.get("debtToEquity", 0),
            
            # Profitability
            "profit_margin": info.get("profitMargins", 0),
            "operating_margin": info.get("operatingMargins", 0),
            "roe": info.get("returnOnEquity", 0),
            "roa": info.get("returnOnAssets", 0),
            
            # Growth
            "revenue_growth": info.get("revenueGrowth", 0),
            "earnings_growth": info.get("earningsGrowth", 0),
            
            # Dividend
            "dividend_yield": info.get("dividendYield", 0),
            "payout_ratio": info.get("payoutRatio", 0),
            
            # Other
            "beta": info.get("beta", 1.0),
            "shares_outstanding": info.get("sharesOutstanding", 0),
            
            # Data quality flag
            "data_completeness": calculate_completeness(info)
        }
        
        # Save to file
        output_path = Path(output_dir) / f"{ticker.upper()}_fundamentals.json"
        with open(output_path, 'w') as f:
            json.dump(fundamentals, f, indent=2)
        
        print(f"[OK] Fundamentals saved to {output_path}")
        return fundamentals
        
    except Exception as e:
        error_data = {
            "error": str(e),
            "ticker": ticker,
            "timestamp": datetime.now().isoformat()
        }
        
        # Still save error to file for workflow continuity
        output_path = Path(output_dir) / f"{ticker.upper()}_fundamentals.json"
        with open(output_path, 'w') as f:
            json.dump(error_data, f, indent=2)
        
        print(f"[ERROR] Error fetching fundamentals: {e}", file=sys.stderr)
        return error_data


def calculate_completeness(info: dict) -> float:
    """Calculate data completeness percentage based on key fields."""
    required_fields = [
        "currentPrice", "marketCap", "totalAssets", "totalDebt",
        "totalRevenue", "netIncomeToCommon", "operatingCashflow"
    ]
    
    available = sum(1 for field in required_fields if info.get(field, 0) != 0)
    return round((available / len(required_fields)) * 100, 1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_stock_fundamentals.py TICKER [output_dir]")
        sys.exit(1)
    
    ticker = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else ".tmp"
    
    result = fetch_stock_fundamentals(ticker, output_dir)
    
    if "error" in result:
        sys.exit(1)
