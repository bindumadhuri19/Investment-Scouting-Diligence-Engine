"""
Synthesize investment analysis using Claude API.
Generates AI-powered risk summary, red flags, and investment recommendation.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def synthesize_with_claude(ticker: str, output_dir: str = ".tmp") -> dict:
    """
    Generate AI synthesis of investment analysis using Claude.
    
    Args:
        ticker: Stock symbol
        output_dir: Directory containing analysis JSON files
        
    Returns:
        dict: Claude synthesis with recommendation
    """
    try:
        # Load all cached data
        data = load_analysis_data(ticker, output_dir)
        
        # Check for API key
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return create_fallback_synthesis(ticker, data, output_dir)
        
        # Build prompt
        prompt = build_synthesis_prompt(ticker, data)
        
        # Call Claude API
        client = Anthropic(api_key=api_key)
        
        # Try multiple model versions for compatibility
        # Order: Latest stable -> Fallback options
        # NOTE: Model availability may vary by API key tier and region
        models_to_try = [
            "claude-sonnet-4-20250514",     # Claude Sonnet 4.5 (May 2025) - LATEST
            "claude-3-5-sonnet-20241022",   # Claude 3.5 Sonnet (Oct 2024)
            "claude-3-5-sonnet-20240620",   # Claude 3.5 Sonnet (June 2024)
            "claude-3-haiku-20240307",      # Claude 3 Haiku (faster, cheaper)
            "claude-3-sonnet-20240229"      # Claude 3 Sonnet
        ]
        
        message = None
        last_error = None
        successful_model = None
        
        for model in models_to_try:
            try:
                message = client.messages.create(
                    model=model,
                    max_tokens=2000,
                    temperature=0.3,  # Lower temp for more deterministic analysis
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )
                successful_model = model
                break  # Success, exit loop
            except Exception as e:
                last_error = e
                continue  # Try next model
        
        if message is None:
            # All models failed - raise to trigger fallback
            raise last_error
        
        # Log which model worked (for debugging)
        if os.getenv("DEBUG", "false").lower() == "true":
            print(f"[DEBUG] Using Claude model: {successful_model}", file=sys.stderr)
        
        # Parse response
        response_text = message.content[0].text
        
        # Try to extract JSON from response
        synthesis = extract_json_from_response(response_text)
        
        if not synthesis:
            # If JSON parsing fails, create structured response from text
            synthesis = {
                "ticker": ticker.upper(),
                "timestamp": datetime.now().isoformat(),
                "risk_summary": response_text[:500],  # First 500 chars
                "red_flags": ["Unable to parse structured response"],
                "opportunities": [],
                "investment_recommendation": "HOLD",
                "confidence_score": 5,
                "reasoning": "Analysis generated but response parsing failed",
                "next_steps": ["Manual review required"],
                "raw_response": response_text
            }
        else:
            synthesis["ticker"] = ticker.upper()
            synthesis["timestamp"] = datetime.now().isoformat()
        
        # Save to file
        output_path = Path(output_dir) / f"{ticker.upper()}_synthesis.json"
        with open(output_path, 'w') as f:
            json.dump(synthesis, f, indent=2)
        
        print(f"[OK] Synthesis saved to {output_path}")
        print(f"[OK] Recommendation: {synthesis.get('investment_recommendation', 'N/A')}")
        print(f"[OK] Confidence: {synthesis.get('confidence_score', 'N/A')}/10")
        
        return synthesis
        
    except Exception as e:
        # If Claude API fails, use fallback synthesis
        print(f"[WARN] Claude API error: {str(e)[:100]}...", file=sys.stderr)
        print(f"[INFO] Using rule-based fallback synthesis", file=sys.stderr)
        return create_fallback_synthesis(ticker, data, output_dir)


def load_analysis_data(ticker: str, output_dir: str) -> dict:
    """Load all analysis JSON files for the ticker."""
    data = {}
    
    files = {
        "fundamentals": f"{ticker}_fundamentals.json",
        "analysis": f"{ticker}_analysis.json",
        "sentiment": f"{ticker}_news.json",
        "sec": f"{ticker}_sec_filings.json"
    }
    
    for key, filename in files.items():
        file_path = Path(output_dir) / filename
        if file_path.exists():
            with open(file_path, 'r') as f:
                data[key] = json.load(f)
        else:
            data[key] = {}
    
    return data


def build_synthesis_prompt(ticker: str, data: dict) -> str:
    """Build comprehensive prompt for Claude."""
    fundamentals = data.get("fundamentals", {})
    analysis = data.get("analysis", {})
    sentiment = data.get("sentiment", {})
    sec = data.get("sec", {})
    
    prompt = f"""You are an expert investment analyst conducting due diligence on {ticker}.

**Company Data**:
- Company: {fundamentals.get('company_name', 'N/A')}
- Sector: {fundamentals.get('sector', 'N/A')}
- Market Cap: ${fundamentals.get('market_cap', 0):,.0f}
- Current Price: ${fundamentals.get('current_price', 0):.2f}
- P/E Ratio: {fundamentals.get('pe_ratio', 'N/A')}
- Revenue: ${fundamentals.get('revenue', 0):,.0f}
- Net Income: ${fundamentals.get('net_income', 0):,.0f}

**Risk Metrics**:
- Altman Z-Score: {analysis.get('altman_zscore', 'N/A')} (Zone: {analysis.get('zscore_zone', 'N/A')})
- Debt/Equity: {analysis.get('debt_to_equity', 'N/A')} (Zone: {analysis.get('debt_zone', 'N/A')})
- Current Ratio: {analysis.get('current_ratio', 'N/A')} (Zone: {analysis.get('liquidity_zone', 'N/A')})
- OCF/Net Income: {analysis.get('ocf_to_ni', 'N/A')}
- Risk Flags: {', '.join(analysis.get('risk_flags', [])) if analysis.get('risk_flags') else 'None'}

**Sentiment Analysis (30-day)**:
- Total Articles: {sentiment.get('total_articles', 0)}
- Sentiment Score: {sentiment.get('sentiment_score', 'N/A')}/100 (Zone: {sentiment.get('sentiment_zone', 'N/A')})
- Negative Articles: {sentiment.get('negative_pct', 0)}%
- Top Concerns: {', '.join(sentiment.get('top_negative_keywords', [])) if sentiment.get('top_negative_keywords') else 'None'}

**Recent News Headlines**:
"""
    
    # Add flagged articles
    flagged = sentiment.get('flagged_articles', [])
    if flagged:
        for i, article in enumerate(flagged[:3], 1):
            prompt += f"\n{i}. {article.get('title', 'N/A')} ({article.get('source', 'Unknown')})"
    else:
        prompt += "\nNo negative news flagged"
    
    prompt += f"""

**SEC Filing**:
- Latest Filing: {sec.get('filing_type', 'N/A')} on {sec.get('filing_date', 'N/A')}
- Summary: {sec.get('summary', 'Not available')}

**Task**: Provide a structured investment analysis in JSON format. RESPOND WITH VALID JSON ONLY:

{{
  "risk_summary": "2-3 sentence overview of overall risk profile",
  "red_flags": ["specific concern 1", "specific concern 2", "..."],
  "opportunities": ["positive signal 1", "positive signal 2", "..."],
  "investment_recommendation": "BUY" or "HOLD" or "SELL",
  "confidence_score": 1-10,
  "reasoning": "Explain your recommendation in 3-4 sentences based on the data provided",
  "next_steps": ["Further diligence action 1", "Further diligence action 2"]
}}

**Guidelines**:
- Be objective and data-driven. Only reference data provided above.
- Flag legitimate concerns only (avoid over-flagging).
- If data is insufficient, note in reasoning and lower confidence score.
- Confidence score reflects data quality: incomplete data = lower confidence.
- Consider all three risk types: financial (Z-Score, debt), sentiment (news), and regulatory (SEC).
- BUY = Z-Score green + positive sentiment + strong fundamentals
- HOLD = Mixed signals or insufficient data
- SELL = Z-Score red + negative sentiment + multiple red flags

RESPOND WITH VALID JSON ONLY. No additional text.
"""
    
    return prompt


def extract_json_from_response(response_text: str) -> dict:
    """Extract and parse JSON from Claude's response."""
    try:
        # Try direct JSON parse first
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Try to find JSON in text (Claude sometimes adds explanation before/after)
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        return None


def create_fallback_synthesis(ticker: str, data: dict, output_dir: str) -> dict:
    """Create rule-based synthesis when Claude API unavailable."""
    analysis = data.get("analysis", {})
    sentiment = data.get("sentiment", {})
    
    # Rule-based recommendation
    zscore = analysis.get('altman_zscore')
    zscore_zone = analysis.get('zscore_zone', 'yellow')
    debt_ratio = analysis.get('debt_to_equity')
    sentiment_score = sentiment.get('sentiment_score', 50)
    risk_flags = analysis.get('risk_flags', [])
    
    # SELL conditions
    if zscore and zscore < 1.8:
        recommendation = "SELL"
        confidence = 8
        reasoning = "High bankruptcy risk based on Altman Z-Score in distress zone (< 1.8)."
    elif sentiment_score and sentiment_score < 35:
        recommendation = "SELL"
        confidence = 6
        reasoning = "Strongly negative market sentiment and media coverage indicate significant concerns."
    elif len(risk_flags) >= 5:
        recommendation = "SELL"
        confidence = 7
        reasoning = f"Multiple red flags detected ({len(risk_flags)} issues) indicating elevated risk."
    
    # BUY conditions (more balanced)
    elif zscore and zscore > 3.0 and sentiment_score >= 50:
        recommendation = "BUY"
        confidence = 8 if sentiment_score > 60 else 7
        reasoning = f"Strong financial health (Z-Score: {zscore:.1f}) with {'positive' if sentiment_score > 60 else 'neutral'} market sentiment."
    elif zscore and zscore > 2.5 and debt_ratio and debt_ratio < 0.5 and sentiment_score >= 55:
        recommendation = "BUY"
        confidence = 7
        reasoning = f"Solid financials (Z-Score: {zscore:.1f}, low debt) with favorable sentiment."
    
    # HOLD conditions
    elif zscore and 1.8 <= zscore <= 3.0:
        recommendation = "HOLD"
        confidence = 5
        reasoning = f"Gray zone Z-Score ({zscore:.1f}) requires careful monitoring before investment."
    else:
        recommendation = "HOLD"
        confidence = 4
        reasoning = "Mixed signals - limited data available for confident recommendation."
    
    synthesis = {
        "ticker": ticker.upper(),
        "timestamp": datetime.now().isoformat(),
        "risk_summary": f"Rule-based analysis (Claude API unavailable). Z-Score: {zscore_zone}, Sentiment: {sentiment.get('sentiment_zone', 'N/A')}",
        "red_flags": risk_flags if risk_flags else ["Limited analysis - manual review recommended"],
        "opportunities": [],
        "investment_recommendation": recommendation,
        "confidence_score": confidence,
        "reasoning": reasoning,
        "next_steps": ["Enable Claude API for full AI synthesis", "Manual analyst review required"],
        "note": "Auto-generated fallback (AI synthesis unavailable)"
    }
    
    output_path = Path(output_dir) / f"{ticker.upper()}_synthesis.json"
    with open(output_path, 'w') as f:
        json.dump(synthesis, f, indent=2)
    
    print(f"[WARN] Using fallback synthesis (Claude API not configured)")
    print(f"[OK] Synthesis saved to {output_path}")
    
    return synthesis


def create_error_synthesis(ticker: str, error_msg: str, output_dir: str) -> dict:
    """Create error response when synthesis fails."""
    synthesis = {
        "error": f"Synthesis failed: {error_msg}",
        "ticker": ticker.upper(),
        "timestamp": datetime.now().isoformat(),
        "investment_recommendation": "HOLD",
        "confidence_score": 1,
        "reasoning": "Unable to generate analysis due to error",
        "next_steps": ["Manual review required", "Check API configuration"]
    }
    
    output_path = Path(output_dir) / f"{ticker.upper()}_synthesis.json"
    with open(output_path, 'w') as f:
        json.dump(synthesis, f, indent=2)
    
    print(f"[ERROR] Synthesis error: {error_msg}", file=sys.stderr)
    return synthesis


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python synthesize_with_claude.py TICKER [output_dir]")
        print("  Reads from: .tmp/TICKER_*.json")
        print("  Writes to: .tmp/TICKER_synthesis.json")
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    output_dir = sys.argv[2] if len(sys.argv) > 2 else ".tmp"
    
    result = synthesize_with_claude(ticker, output_dir)
    
    if "error" in result:
        sys.exit(1)
