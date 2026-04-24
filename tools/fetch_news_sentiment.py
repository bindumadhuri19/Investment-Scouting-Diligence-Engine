"""
Fetch news articles and calculate sentiment score using NewsAPI.
Output: JSON file with articles, sentiment analysis, and flagged keywords.
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
import requests
from collections import Counter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Negative keywords (red flags)
NEGATIVE_KEYWORDS = [
    # Financial distress
    "bankruptcy", "insolvent", "default", "debt crisis", "liquidity crisis",
    # Legal issues
    "lawsuit", "litigation", "settlement", "sec investigation", "fraud", "class action",
    # Accounting concerns
    "restatement", "accounting error", "misstatement", "audit issue", "going concern",
    # Operational problems
    "layoffs", "plant closure", "recall", "safety issue", "regulatory violation",
    # Market concerns
    "downgrade", "earnings miss", "guidance cut", "weak outlook", "disappointing results"
]

# Positive keywords
POSITIVE_KEYWORDS = [
    "record revenue", "beat expectations", "strong quarter", "market share gain",
    "acquisition", "partnership", "innovation", "buyback", "dividend increase",
    "upgrade", "outperform", "bullish", "growth acceleration"
]


def fetch_news_sentiment(ticker: str, output_dir: str = ".tmp", days: int = 30) -> dict:
    """
    Fetch news articles and calculate sentiment score.
    
    Args:
        ticker: Stock symbol (e.g., "AAPL")
        output_dir: Directory to save JSON output
        days: Number of days to look back (default 30)
        
    Returns:
        dict: News and sentiment data
    """
    try:
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Get API key from environment
        api_key = os.getenv("NEWSAPI_KEY")
        
        if not api_key:
            return create_no_api_key_response(ticker, output_dir)
        
        # Calculate date range
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days)
        
        # NewsAPI endpoint
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": f"{ticker}",
            "from": from_date.strftime("%Y-%m-%d"),
            "to": to_date.strftime("%Y-%m-%d"),
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 100,  # Max for free tier
            "apiKey": api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 429:
            return create_rate_limit_response(ticker, output_dir)
        elif response.status_code != 200:
            return create_error_response(ticker, f"NewsAPI error: {response.status_code}", output_dir)
        
        data = response.json()
        articles = data.get("articles", [])
        
        if len(articles) < 5:
            return create_insufficient_data_response(ticker, articles, output_dir)
        
        # Analyze sentiment
        sentiment_analysis = analyze_articles(articles, ticker)
        
        # Save to file
        output_path = Path(output_dir) / f"{ticker.upper()}_news.json"
        with open(output_path, 'w') as f:
            json.dump(sentiment_analysis, f, indent=2)
        
        print(f"[OK] News sentiment saved to {output_path}")
        return sentiment_analysis
        
    except requests.Timeout:
        return create_error_response(ticker, "NewsAPI timeout", output_dir)
    except Exception as e:
        return create_error_response(ticker, str(e), output_dir)


def analyze_articles(articles: list, ticker: str) -> dict:
    """Perform keyword-based sentiment analysis on articles."""
    negative_articles = []
    positive_articles = []
    neutral_articles = []
    all_negative_keywords = []
    
    for article in articles:
        text = f"{article.get('title', '')} {article.get('description', '')}".lower()
        
        # Check for keywords
        found_negative = [kw for kw in NEGATIVE_KEYWORDS if kw in text]
        found_positive = [kw for kw in POSITIVE_KEYWORDS if kw in text]
        
        article_data = {
            "title": article.get("title", ""),
            "source": article.get("source", {}).get("name", "Unknown"),
            "publishedAt": article.get("publishedAt", ""),
            "url": article.get("url", ""),
            "negative_keywords": found_negative,
            "positive_keywords": found_positive
        }
        
        if found_negative:
            negative_articles.append(article_data)
            all_negative_keywords.extend(found_negative)
        elif found_positive:
            positive_articles.append(article_data)
        else:
            neutral_articles.append(article_data)
    
    total = len(articles)
    negative_count = len(negative_articles)
    positive_count = len(positive_articles)
    neutral_count = len(neutral_articles)
    
    # Calculate sentiment score (0-100, where 0=very negative, 50=neutral, 100=very positive)
    sentiment_score = calculate_sentiment_score(negative_count, positive_count, total)
    
    # Determine zone
    if sentiment_score >= 60:
        zone = "green"
    elif sentiment_score >= 40:
        zone = "yellow"
    else:
        zone = "red"
    
    # Get most common negative keywords
    keyword_counts = Counter(all_negative_keywords)
    top_keywords = [kw for kw, count in keyword_counts.most_common(5)]
    
    return {
        "ticker": ticker.upper(),
        "timestamp": datetime.now().isoformat(),
        "total_articles": total,
        "negative_count": negative_count,
        "positive_count": positive_count,
        "neutral_count": neutral_count,
        "negative_pct": round((negative_count / total) * 100, 1) if total > 0 else 0,
        "positive_pct": round((positive_count / total) * 100, 1) if total > 0 else 0,
        "sentiment_score": sentiment_score,
        "sentiment_zone": zone,
        "top_negative_keywords": top_keywords,
        "flagged_articles": negative_articles[:5],  # Top 5 concerning articles
        "data_available": True
    }


def calculate_sentiment_score(negative: int, positive: int, total: int) -> int:
    """Calculate sentiment score 0-100."""
    if total == 0:
        return 50  # Neutral
    
    # Formula: ((positive - negative) / total * 50) + 50
    # This maps to: all negative = 0, all positive = 100, equal mix = 50
    score = ((positive - negative) / total * 50) + 50
    return max(0, min(100, round(score)))


def create_no_api_key_response(ticker: str, output_dir: str) -> dict:
    """Create response when API key not configured."""
    data = {
        "error": "NewsAPI key not configured in .env file",
        "ticker": ticker.upper(),
        "timestamp": datetime.now().isoformat(),
        "data_available": False,
        "note": "Set NEWSAPI_KEY in .env to enable news sentiment analysis"
    }
    
    output_path = Path(output_dir) / f"{ticker.upper()}_news.json"
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"[WARN] NewsAPI key not configured", file=sys.stderr)
    return data


def create_rate_limit_response(ticker: str, output_dir: str) -> dict:
    """Create response when rate limited."""
    data = {
        "error": "NewsAPI rate limit exceeded (500 requests/day on free tier)",
        "ticker": ticker.upper(),
        "timestamp": datetime.now().isoformat(),
        "data_available": False
    }
    
    output_path = Path(output_dir) / f"{ticker.upper()}_news.json"
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"[WARN] NewsAPI rate limit exceeded", file=sys.stderr)
    return data


def create_insufficient_data_response(ticker: str, articles: list, output_dir: str) -> dict:
    """Create response when article count is too low."""
    data = {
        "ticker": ticker.upper(),
        "timestamp": datetime.now().isoformat(),
        "total_articles": len(articles),
        "warning": "Insufficient news data (< 5 articles in 30 days)",
        "sentiment_score": None,
        "sentiment_zone": "N/A",
        "data_available": False,
        "note": "Ticker may be low-profile or delisted"
    }
    
    output_path = Path(output_dir) / f"{ticker.upper()}_news.json"
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"[WARN] Insufficient news data for {ticker}", file=sys.stderr)
    return data


def create_error_response(ticker: str, error_msg: str, output_dir: str) -> dict:
    """Create standardized error response."""
    data = {
        "error": error_msg,
        "ticker": ticker.upper(),
        "timestamp": datetime.now().isoformat(),
        "data_available": False
    }
    
    output_path = Path(output_dir) / f"{ticker.upper()}_news.json"
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✗ News fetch failed: {error_msg}", file=sys.stderr)
    return data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_news_sentiment.py TICKER [output_dir] [days]")
        sys.exit(1)
    
    ticker = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else ".tmp"
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    
    result = fetch_news_sentiment(ticker, output_dir, days)
    
    if "error" in result or not result.get("data_available"):
        sys.exit(1)
