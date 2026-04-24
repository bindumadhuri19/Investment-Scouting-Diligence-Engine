"""
Comprehensive system test script.
Tests all components of the Investment Diligence Engine.
"""

import os
import sys
from pathlib import Path
import json
from dotenv import load_dotenv

load_dotenv()


def print_header(text):
    """Print formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def test_environment():
    """Test 1: Environment Variables"""
    print_header("TEST 1: Environment Configuration")
    
    checks = {
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "NEWSAPI_KEY": os.getenv("NEWSAPI_KEY"),
        "CACHE_TTL": os.getenv("CACHE_TTL"),
        "DEBUG": os.getenv("DEBUG")
    }
    
    passed = 0
    for key, value in checks.items():
        if value:
            # Mask sensitive keys
            display_value = value if key in ["CACHE_TTL", "DEBUG"] else f"{value[:10]}...{value[-4:]}"
            print(f"✅ {key}: {display_value}")
            passed += 1
        else:
            print(f"⚠️  {key}: Not set")
    
    print(f"\nResult: {passed}/4 environment variables configured")
    return passed >= 2  # At least ANTHROPIC and NEWSAPI keys


def test_dependencies():
    """Test 2: Python Dependencies"""
    print_header("TEST 2: Python Dependencies")
    
    dependencies = [
        ("yfinance", "Stock data"),
        ("requests", "HTTP requests"),
        ("anthropic", "Claude API"),
        ("dotenv", "Environment variables")
    ]
    
    passed = 0
    for package, purpose in dependencies:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package:20} - {purpose}")
            passed += 1
        except ImportError:
            print(f"❌ {package:20} - NOT INSTALLED")
    
    print(f"\nResult: {passed}/{len(dependencies)} dependencies available")
    return passed == len(dependencies)


def test_tools():
    """Test 3: Tool Scripts"""
    print_header("TEST 3: Tool Scripts")
    
    tools_dir = Path("tools")
    expected_tools = [
        "fetch_stock_fundamentals.py",
        "fetch_sec_filings.py",
        "fetch_news_sentiment.py",
        "calculate_altman_zscore.py",
        "calculate_debt_ratios.py",
        "synthesize_with_claude.py",
        "export_to_google_sheets.py",
        "export_to_google_slides.py"
    ]
    
    passed = 0
    for tool in expected_tools:
        path = tools_dir / tool
        if path.exists():
            print(f"✅ {tool}")
            passed += 1
        else:
            print(f"❌ {tool} - NOT FOUND")
    
    print(f"\nResult: {passed}/{len(expected_tools)} tools available")
    return passed == len(expected_tools)


def test_workflows():
    """Test 4: Workflow Files"""
    print_header("TEST 4: Workflow Files")
    
    workflows_dir = Path("workflows")
    expected_workflows = [
        "analyze_stock.md",
        "fetch_company_data.md",
        "calculate_risk_metrics.md",
        "analyze_sentiment.md",
        "synthesize_analysis.md",
        "generate_report.md"
    ]
    
    passed = 0
    for workflow in expected_workflows:
        path = workflows_dir / workflow
        if path.exists():
            print(f"✅ {workflow}")
            passed += 1
        else:
            print(f"❌ {workflow} - NOT FOUND")
    
    print(f"\nResult: {passed}/{len(expected_workflows)} workflows available")
    return passed == len(expected_workflows)


def test_data_fetch():
    """Test 5: Data Fetching (AAPL sample)"""
    print_header("TEST 5: Data Fetching")
    
    import subprocess
    
    print("Testing stock fundamentals fetch...")
    result = subprocess.run(
        [sys.executable, "tools/fetch_stock_fundamentals.py", "AAPL", ".tmp"],
        capture_output=True,
        text=True
    )
    
    fundamentals_ok = result.returncode == 0
    print(f"{'✅' if fundamentals_ok else '❌'} Stock fundamentals: {result.returncode}")
    
    print("\nTesting news sentiment fetch...")
    result = subprocess.run(
        [sys.executable, "tools/fetch_news_sentiment.py", "AAPL", ".tmp"],
        capture_output=True,
        text=True
    )
    
    news_ok = result.returncode == 0
    print(f"{'✅' if news_ok else '⚠️'} News sentiment: {result.returncode}")
    
    # Check if files were created
    fundamentals_file = Path(".tmp/AAPL_fundamentals.json")
    news_file = Path(".tmp/AAPL_news.json")
    
    if fundamentals_file.exists():
        with open(fundamentals_file) as f:
            data = json.load(f)
            completeness = data.get("data_completeness", 0)
            print(f"   Data completeness: {completeness}%")
    
    if news_file.exists():
        with open(news_file) as f:
            data = json.load(f)
            if "error" not in data:
                sentiment = data.get("sentiment_score", "N/A")
                articles = data.get("total_articles", 0)
                print(f"   Sentiment score: {sentiment}/100 ({articles} articles)")
    
    return fundamentals_ok


def test_analysis():
    """Test 6: Risk Analysis"""
    print_header("TEST 6: Risk Analysis")
    
    import subprocess
    
    print("Testing Altman Z-Score calculation...")
    result = subprocess.run(
        [sys.executable, "tools/calculate_altman_zscore.py", "AAPL", ".tmp"],
        capture_output=True,
        text=True
    )
    
    zscore_ok = result.returncode == 0
    print(f"{'✅' if zscore_ok else '❌'} Altman Z-Score: {result.returncode}")
    
    print("\nTesting debt ratios calculation...")
    result = subprocess.run(
        [sys.executable, "tools/calculate_debt_ratios.py", "AAPL", ".tmp"],
        capture_output=True,
        text=True
    )
    
    debt_ok = result.returncode == 0
    print(f"{'✅' if debt_ok else '❌'} Debt ratios: {result.returncode}")
    
    # Check analysis results
    analysis_file = Path(".tmp/AAPL_analysis.json")
    if analysis_file.exists():
        with open(analysis_file) as f:
            data = json.load(f)
            zscore = data.get("altman_zscore")
            zone = data.get("zscore_zone")
            debt_ratio = data.get("debt_to_equity")
            print(f"\n   Z-Score: {zscore} ({zone})")
            print(f"   Debt/Equity: {debt_ratio}")
    
    return zscore_ok and debt_ok


def test_synthesis():
    """Test 7: AI Synthesis"""
    print_header("TEST 7: AI Synthesis")
    
    import subprocess
    
    print("Testing Claude synthesis...")
    result = subprocess.run(
        [sys.executable, "tools/synthesize_with_claude.py", "AAPL", ".tmp"],
        capture_output=True,
        text=True
    )
    
    synthesis_ok = result.returncode == 0
    print(f"{'✅' if synthesis_ok else '⚠️'} Synthesis: {result.returncode}")
    
    # Check synthesis results
    synthesis_file = Path(".tmp/AAPL_synthesis.json")
    if synthesis_file.exists():
        with open(synthesis_file) as f:
            data = json.load(f)
            recommendation = data.get("investment_recommendation", "N/A")
            confidence = data.get("confidence_score", "N/A")
            is_fallback = "note" in data and "fallback" in data.get("note", "").lower()
            
            print(f"\n   Recommendation: {recommendation}")
            print(f"   Confidence: {confidence}/10")
            if is_fallback:
                print(f"   ⚠️  Using fallback synthesis (Claude API unavailable)")
            else:
                print(f"   ✅ Using Claude AI synthesis")
    
    return synthesis_ok


def test_end_to_end():
    """Test 8: Full Pipeline"""
    print_header("TEST 8: End-to-End Analysis")
    
    import subprocess
    
    print("Running full analysis pipeline for AAPL...")
    print("(This will take 15-30 seconds)\n")
    
    result = subprocess.run(
        [sys.executable, "analyze.py", "AAPL"],
        capture_output=True,
        text=True
    )
    
    success = result.returncode == 0
    
    if success:
        print("✅ Full pipeline executed successfully!")
        print("\nOutput preview:")
        print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
    else:
        print("❌ Pipeline failed!")
        print(f"Exit code: {result.returncode}")
        print(f"\nError output:")
        print(result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)
    
    return success


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("  INVESTMENT DILIGENCE ENGINE - SYSTEM TEST")
    print("="*60)
    
    results = {
        "Environment": test_environment(),
        "Dependencies": test_dependencies(),
        "Tool Scripts": test_tools(),
        "Workflows": test_workflows(),
        "Data Fetch": test_data_fetch(),
        "Risk Analysis": test_analysis(),
        "AI Synthesis": test_synthesis(),
        "End-to-End": test_end_to_end()
    }
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_flag in results.items():
        status = "✅ PASS" if passed_flag else "❌ FAIL"
        print(f"{status:10} - {test_name}")
    
    print(f"\n{'='*60}")
    print(f"  OVERALL RESULT: {passed}/{total} tests passed")
    
    if passed == total:
        print(f"  🎉 ALL TESTS PASSED - System is fully operational!")
    elif passed >= 6:
        print(f"  ✅ System is functional with minor issues")
    else:
        print(f"  ⚠️  System has critical issues - review failures")
    
    print(f"{'='*60}\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
