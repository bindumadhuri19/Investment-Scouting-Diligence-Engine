"""
Main orchestrator script for Investment Scouting & Diligence Engine.
Follows WAT framework: Reads workflows, executes tools in sequence.

Usage:
    python analyze.py TICKER
    
Example:
    python analyze.py AAPL
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import subprocess
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main(ticker: str):
    """
    Main orchestration following workflows/analyze_stock.md workflow.
    
    Args:
        ticker: Stock symbol to analyze
    """
    print(f"\n{'='*60}")
    print(f"Investment Diligence Analysis: {ticker.upper()}")
    print(f"{'='*60}\n")
    
    start_time = datetime.now()
    
    # Check cache
    if check_cache(ticker):
        print(f"[OK] Using cached data (< 1 hour old)")
        use_cache = True
    else:
        print(f"[*] Fetching fresh data...")
        use_cache = False
    
    # Step 1: Fetch company data (parallel workflow)
    print(f"\n[1/5] Fetching company data...")
    if not use_cache:
        success = fetch_company_data(ticker)
        if not success:
            print(f"[ERROR] Failed to fetch sufficient data. Exiting.")
            return False
    
    # Step 2: Calculate risk metrics
    print(f"\n[2/5] Calculating risk metrics...")
    calculate_risk_metrics(ticker)
    
    # Step 3: Analyze sentiment (already done in step 1, verify file exists)
    print(f"\n[3/5] Analyzing sentiment...")
    verify_sentiment_data(ticker)
    
    # Step 4: Synthesize with Claude
    print(f"\n[4/5] Generating AI synthesis...")
    synthesize_analysis(ticker)
    
    # Step 5: Generate reports
    print(f"\n[5/5] Generating reports...")
    export_reports(ticker)
    
    # Summary
    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"\n{'='*60}")
    print(f"[OK] Analysis complete in {elapsed:.1f}s")
    print(f"{'='*60}\n")
    
    # Display summary
    display_summary(ticker)
    
    return True


def check_cache(ticker: str) -> bool:
    """Check if cached data exists and is fresh (<1 hour)."""
    cache_files = [
        f".tmp/{ticker.upper()}_fundamentals.json",
        f".tmp/{ticker.upper()}_news.json"
    ]
    
    cache_ttl = int(os.getenv("CACHE_TTL", "3600"))
    
    for cache_file in cache_files:
        path = Path(cache_file)
        if not path.exists():
            return False
        
        # Check age
        age = datetime.now().timestamp() - path.stat().st_mtime
        if age > cache_ttl:
            return False
    
    return True


def fetch_company_data(ticker: str) -> bool:
    """
    Execute workflows/fetch_company_data.md
    Runs 3 tools in parallel (simulated with sequential for simplicity in MVP)
    """
    success_count = 0
    
    # Fetch fundamentals
    result = run_tool("fetch_stock_fundamentals.py", ticker)
    if result == 0:
        success_count += 1
    
    # Fetch SEC filings
    result = run_tool("fetch_sec_filings.py", ticker)
    if result == 0:
        success_count += 1
    else:
        print(f"  [WARN] SEC filing fetch failed (non-critical)")
    
    # Fetch news sentiment
    result = run_tool("fetch_news_sentiment.py", ticker)
    if result == 0:
        success_count += 1
    else:
        print(f"  [WARN] News sentiment fetch failed (check NEWSAPI_KEY in .env)")
    
    # Need at least fundamentals to proceed
    return success_count >= 1


def calculate_risk_metrics(ticker: str):
    """Execute workflows/calculate_risk_metrics.md"""
    # Calculate Z-Score
    run_tool("calculate_altman_zscore.py", ticker)
    
    # Calculate debt ratios
    run_tool("calculate_debt_ratios.py", ticker)


def verify_sentiment_data(ticker: str):
    """Verify sentiment data exists (already fetched in step 1)"""
    sentiment_file = Path(f".tmp/{ticker.upper()}_news.json")
    if sentiment_file.exists():
        print(f"  [OK] Sentiment data available")
    else:
        print(f"  [WARN] Sentiment data not available")


def synthesize_analysis(ticker: str):
    """Execute workflows/synthesize_analysis.md"""
    result = run_tool("synthesize_with_claude.py", ticker)
    if result != 0:
        print(f"  [WARN] AI synthesis failed (check ANTHROPIC_API_KEY in .env)")
        print(f"  [INFO] Fallback: Rule-based analysis will be used")


def export_reports(ticker: str):
    """Execute workflows/generate_report.md"""
    # Export to Google Sheets
    print(f"  Exporting to Google Sheets...")
    run_tool("export_to_google_sheets.py", ticker)
    
    # Export to Google Slides
    print(f"  Exporting to Google Slides...")
    run_tool("export_to_google_slides.py", ticker)


def run_tool(script_name: str, ticker: str) -> int:
    """
    Execute a tool script.
    
    Args:
        script_name: Tool script filename
        ticker: Stock symbol
        
    Returns:
        int: Return code (0 = success)
    """
    script_path = Path("tools") / script_name
    
    if not script_path.exists():
        print(f"  [ERROR] Tool not found: {script_path}")
        return 1
    
    # Run tool
    result = subprocess.run(
        [sys.executable, str(script_path), ticker, ".tmp"],
        capture_output=True,
        text=True
    )
    
    # Print output if debug enabled
    if os.getenv("DEBUG", "false").lower() == "true":
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    
    return result.returncode


def display_summary(ticker: str):
    """Display analysis summary from cached results."""
    try:
        # Load synthesis
        synthesis_path = Path(f".tmp/{ticker.upper()}_synthesis.json")
        if not synthesis_path.exists():
            print("Summary not available")
            return
        
        with open(synthesis_path, 'r') as f:
            synthesis = json.load(f)
        
        # Load analysis
        analysis_path = Path(f".tmp/{ticker.upper()}_analysis.json")
        if analysis_path.exists():
            with open(analysis_path, 'r') as f:
                analysis = json.load(f)
        else:
            analysis = {}
        
        # Display
        print(f"\n[ANALYSIS SUMMARY]")
        print(f"{'-'*60}")
        print(f"Ticker: {ticker.upper()}")
        print(f"")
        print(f"Financial Health:")
        print(f"  Altman Z-Score: {analysis.get('altman_zscore', 'N/A')} ({analysis.get('zscore_zone', 'N/A')})")
        print(f"  Debt/Equity: {analysis.get('debt_to_equity', 'N/A')} ({analysis.get('debt_zone', 'N/A')})")
        print(f"")
        print(f"AI Recommendation: {synthesis.get('investment_recommendation', 'N/A')}")
        print(f"Confidence: {synthesis.get('confidence_score', 'N/A')}/10")
        print(f"")
        print(f"Reasoning: {synthesis.get('reasoning', 'N/A')}")
        print(f"")
        
        red_flags = synthesis.get('red_flags', [])
        if red_flags:
            print(f"[!] Red Flags:")
            for flag in red_flags[:3]:  # Show top 3
                print(f"  - {flag}")
            if len(red_flags) > 3:
                print(f"  ... and {len(red_flags) - 3} more")
        
        print(f"\n[*] Results saved to .tmp/{ticker.upper()}_*.json")
        
        # Show export locations
        sheets_export = Path(f".tmp/{ticker.upper()}_sheet_export.json")
        if sheets_export.exists():
            print(f"[*] Google Sheets: .tmp/{ticker.upper()}_sheet_export.json")
        
        slides_export = Path(f".tmp/{ticker.upper()}_slides_export.json")
        if slides_export.exists():
            print(f"[*] Google Slides: .tmp/{ticker.upper()}_slides_export.json")
        
    except Exception as e:
        print(f"Error displaying summary: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze.py TICKER")
        print("")
        print("Example:")
        print("  python analyze.py AAPL")
        print("  python analyze.py TSLA")
        print("")
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    success = main(ticker)
    
    sys.exit(0 if success else 1)
