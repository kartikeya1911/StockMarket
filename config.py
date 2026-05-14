"""
Configuration for QuantEdge — Stock Market Intelligence Platform

Centralized settings for all modules: UI, data fetching, ML, technical analysis,
portfolio management, news/sentiment, and market overview.

Version: 4.0.0
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# ==================== APPLICATION SETTINGS ====================

APP_TITLE = "QuantEdge"
APP_SUBTITLE = "Stock Market Intelligence Platform"
APP_ICON = "📊"
APP_VERSION = "4.0.0"
APP_AUTHOR = "QuantEdge"

# Currency
CURRENCY_SYMBOL = "₹"
CURRENCY_NAME = "INR"

# Page config
PAGE_TITLE = "QuantEdge — Stock Intelligence"
PAGE_ICON = "📊"
LAYOUT = "wide"

# ==================== NAVIGATION ====================

SIDEBAR_OPTIONS = [
    "📊 Dashboard",
    "🔍 Stock Analysis",
    "🤖 AI Intelligence",
    "📉 Technical Indicators",
    "🔮 Price Prediction",
    "💼 Portfolio Tracker",
    "📰 News & Sentiment",
]

# ==================== MARKET INDICES ====================

MARKET_INDICES = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN",
    "BANK NIFTY": "^NSEBANK",
    "NIFTY IT": "^CNXIT",
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "DOW JONES": "^DJI",
}

# ==================== DATA SETTINGS ====================

DEFAULT_STOCKS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
    "META", "NVDA", "JPM", "V", "WMT"
]

INDIAN_STOCKS = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
    "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS"
]

TIME_PERIODS: Dict[str, str] = {
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "2 Years": "2y",
    "5 Years": "5y",
    "Max": "max"
}

DATA_INTERVALS: Dict[str, str] = {
    "1 Day": "1d",
    "1 Week": "1wk",
    "1 Month": "1mo"
}

# ==================== MACHINE LEARNING ====================

PREDICTION_DAYS = 30
TRAIN_TEST_SPLIT = 0.8
RANDOM_STATE = 42
LOOKBACK_DAYS = 60

# ==================== TECHNICAL INDICATORS ====================

MA_SHORT_PERIOD = 50
MA_LONG_PERIOD = 200
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BB_PERIOD = 20
BB_STD_DEV = 2
ADX_PERIOD = 14
ATR_PERIOD = 14
STOCH_RSI_PERIOD = 14
SUPERTREND_PERIOD = 10
SUPERTREND_MULTIPLIER = 3.0

# ==================== RECOMMENDATION ENGINE WEIGHTS ====================

RECOMMENDATION_WEIGHTS = {
    "technical": 0.30,
    "fundamental": 0.25,
    "sentiment": 0.15,
    "ai_prediction": 0.20,
    "risk": 0.10,
}

RECOMMENDATION_LABELS = {
    (80, 100): "Strong Buy",
    (60, 80): "Buy",
    (40, 60): "Hold",
    (20, 40): "Sell",
    (0, 20): "Strong Sell",
}

# ==================== PORTFOLIO ====================

PORTFOLIO_FILE = "data/portfolio.csv"
PORTFOLIO_DB = "data/portfolio.db"

# ==================== NEWS / SENTIMENT ====================

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "838652a71b7b424c84c4b84dca58978a")
NEWS_SOURCES = "bloomberg,reuters,financial-times,the-wall-street-journal"
NEWS_LANGUAGE = "en"
MAX_NEWS_ARTICLES = 10

# ==================== CHART SETTINGS ====================

CHART_COLORS = {
    "primary": "#00D4FF",
    "positive": "#00C853",
    "negative": "#FF5252",
    "neutral": "#78909C",
    "accent": "#FFD740",
    "info": "#448AFF",
    "warning": "#FF9100",
    "bg_dark": "#0A0E27",
    "card_bg": "rgba(15, 20, 50, 0.85)",
    "border": "rgba(255, 255, 255, 0.06)",
}

CHART_TEMPLATE = "plotly_dark"

# ==================== UI THEME ====================

THEME = {
    "bg_primary": "#0A0E27",
    "bg_secondary": "#111633",
    "bg_card": "rgba(15, 20, 50, 0.85)",
    "text_primary": "#E8EAF6",
    "text_secondary": "#78909C",
    "accent_1": "#00D4FF",
    "accent_2": "#00C853",
    "accent_3": "#FF5252",
    "gradient_1": "linear-gradient(135deg, #00D4FF 0%, #0091EA 100%)",
    "gradient_2": "linear-gradient(135deg, #00C853 0%, #00897B 100%)",
    "gradient_3": "linear-gradient(135deg, #FF5252 0%, #D50000 100%)",
    "gradient_gold": "linear-gradient(135deg, #FFD740 0%, #FF9100 100%)",
    "glass": "rgba(15, 20, 50, 0.85)",
    "glass_border": "rgba(255, 255, 255, 0.06)",
    "blur": "20px",
    "radius": "14px",
    "font_family": "'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif",
}

# ==================== MESSAGES ====================

LOADING_MESSAGES = {
    "fetching_data": "Fetching stock data...",
    "analyzing": "Analyzing stock...",
    "predicting": "Generating predictions...",
    "calculating": "Calculating indicators...",
    "loading_news": "Loading latest news...",
    "ai_analysis": "Running AI analysis engine...",
}

ERROR_MESSAGES = {
    "invalid_ticker": "❌ Invalid stock ticker. Please enter a valid symbol.",
    "no_data": "❌ No data available for this stock.",
    "api_error": "❌ Error fetching data. Please try again later.",
    "prediction_error": "❌ Error generating predictions.",
    "portfolio_error": "❌ Error managing portfolio.",
    "news_error": "❌ Error fetching news. Check your API key.",
}

SUCCESS_MESSAGES = {
    "data_loaded": "✅ Data loaded successfully!",
    "prediction_complete": "✅ Predictions generated successfully!",
    "portfolio_updated": "✅ Portfolio updated successfully!",
    "stock_added": "✅ Stock added to portfolio!",
}

# ==================== HELPERS ====================

def get_date_range(period: str):
    """Calculate start and end dates based on period string."""
    end_date = datetime.now()
    period_days = {
        "1mo": 30, "3mo": 90, "6mo": 180,
        "1y": 365, "2y": 730, "5y": 1825, "max": 3650,
    }
    days = period_days.get(period, 3650)
    start_date = end_date - timedelta(days=days)
    return start_date, end_date
