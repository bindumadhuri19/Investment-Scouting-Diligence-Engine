"""
Fetch SEC EDGAR filings for a given ticker.
Output: JSON file with latest 10-K summary and filing metadata.
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path
import requests
from time import sleep


def fetch_sec_filings(ticker: str, output_dir: str = ".tmp") -> dict:
    """
    Fetch SEC filing data from EDGAR database.
    
    Args:
        ticker: Stock symbol (e.g., "AAPL")
        output_dir: Directory to save JSON output
        
    Returns:
        dict: SEC filing data
    """
    try:
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # SEC EDGAR API endpoint
        headers = {
            'User-Agent': 'Investment Diligence Engine contact@example.com'
        }
        
        # Search for company CIK (Central Index Key)
        ticker_upper = ticker.upper()
        search_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker_upper}&type=10-K&dateb=&owner=exclude&count=1&search_text="
        
        # Get company filings page
        response = requests.get(search_url, headers=headers, timeout=10)
        sleep(0.1)  # Be respectful to SEC servers
        
        if response.status_code != 200:
            return create_error_response(ticker, "SEC EDGAR API unavailable")
        
        # Try to extract filing information from HTML
        # Note: This is a simplified parser. Production would use proper HTML parsing.
        filing_data = {
            "ticker": ticker_upper,
            "timestamp": datetime.now().isoformat(),
            "filing_type": "10-K",
            "filing_date": extract_filing_date(response.text),
            "company_name": extract_company_name(response.text),
            "cik": extract_cik(response.text),
            "accession_number": extract_accession(response.text),
            "filing_url": extract_filing_url(response.text),
            "summary": "SEC 10-K filing data retrieved. Full parsing not implemented in MVP.",
            "data_available": True if extract_filing_date(response.text) else False,
            "note": "MVP implementation - basic metadata only. Production version would parse full 10-K content."
        }
        
        # Save to file
        output_path = Path(output_dir) / f"{ticker_upper}_sec_filings.json"
        with open(output_path, 'w') as f:
            json.dump(filing_data, f, indent=2)
        
        print(f"✓ SEC filings saved to {output_path}")
        return filing_data
        
    except requests.Timeout:
        return create_error_response(ticker, "SEC API timeout")
    except Exception as e:
        return create_error_response(ticker, str(e))


def create_error_response(ticker: str, error_msg: str) -> dict:
    """Create standardized error response and save to file."""
    error_data = {
        "error": error_msg,
        "ticker": ticker.upper(),
        "timestamp": datetime.now().isoformat(),
        "data_available": False
    }
    
    output_path = Path(".tmp") / f"{ticker.upper()}_sec_filings.json"
    with open(output_path, 'w') as f:
        json.dump(error_data, f, indent=2)
    
    print(f"[WARN] SEC filing fetch failed: {error_msg}", file=sys.stderr)
    return error_data


def extract_filing_date(html: str) -> str:
    """Extract most recent filing date from EDGAR HTML."""
    # Look for date pattern like 2024-01-31
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})', html)
    return match.group(0) if match else None


def extract_company_name(html: str) -> str:
    """Extract company name from EDGAR HTML."""
    match = re.search(r'<span class="companyName">([^<]+)', html)
    return match.group(1).strip() if match else "N/A"


def extract_cik(html: str) -> str:
    """Extract CIK number from EDGAR HTML."""
    match = re.search(r'CIK=(\d+)', html)
    return match.group(1) if match else None


def extract_accession(html: str) -> str:
    """Extract accession number from EDGAR HTML."""
    match = re.search(r'Accession Number:\s*(\d+-\d+-\d+)', html)
    return match.group(1) if match else None


def extract_filing_url(html: str) -> str:
    """Extract direct filing URL from EDGAR HTML."""
    match = re.search(r'href="(/Archives/edgar/data/[^"]+)"', html)
    if match:
        return f"https://www.sec.gov{match.group(1)}"
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_sec_filings.py TICKER [output_dir]")
        sys.exit(1)
    
    ticker = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else ".tmp"
    
    result = fetch_sec_filings(ticker, output_dir)
    
    if "error" in result:
        sys.exit(1)
