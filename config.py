"""
Configuration file for Stock Market Analysis Application

Contains all global settings, constants, and API keys:
- Application metadata and UI settings
- Stock data and prediction parameters
- Technical indicator configurations
- Portfolio management settings
- News API credentials
- Theme colors and styling

Version: 2.0.0 - Major rewrite with portfolio enhancements
"""

import os
from datetime import datetime, timedelta

# ==================== APPLICATION SETTINGS ====================

# Application metadata
APP_TITLE = "📈 Stock Market Analysis & Prediction"
APP_ICON = "📊"
APP_VERSION = "2.0.0"

# Currency settings
CURRENCY_SYMBOL = "₹"  # Indian Rupee
CURRENCY_NAME = "INR"

# Page configuration
PAGE_TITLE = "Stock Market Analyzer"
PAGE_ICON = "📈"
LAYOUT = "wide"

# ==================== DATA SETTINGS ====================

# Default stock symbols for quick access
DEFAULT_STOCKS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
    "META", "NVDA", "JPM", "V", "WMT"
]

# Indian stock examples
INDIAN_STOCKS = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
    "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS"
]

# Time period options for data fetching
TIME_PERIODS = {
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "2 Years": "2y",
    "5 Years": "5y",
    "Max": "max"
}

# Data intervals
DATA_INTERVALS = {
    "1 Day": "1d",
    "1 Week": "1wk",
    "1 Month": "1mo"
}

# ==================== MACHINE LEARNING SETTINGS ====================

# Prediction settings
PREDICTION_DAYS = 30  # Number of days to predict into the future
TRAIN_TEST_SPLIT = 0.8  # 80% training, 20% testing
RANDOM_STATE = 42

# Feature engineering
LOOKBACK_DAYS = 60  # Days to look back for feature creation

# ==================== TECHNICAL INDICATORS SETTINGS ====================

# Moving Averages
MA_SHORT_PERIOD = 50   # Short-term moving average
MA_LONG_PERIOD = 200   # Long-term moving average

# RSI Settings
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# MACD Settings
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Bollinger Bands Settings
BB_PERIOD = 20
BB_STD_DEV = 2

# ==================== PORTFOLIO SETTINGS ====================

# Portfolio data file
PORTFOLIO_FILE = "data/portfolio.csv"
PORTFOLIO_DB = "data/portfolio.db"

# ==================== NEWS API SETTINGS ====================

# News API Key (Get free key from: https://newsapi.org/)
# Replace with your own API key
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "838652a71b7b424c84c4b84dca58978a")

# News settings
NEWS_SOURCES = "bloomberg,reuters,financial-times,the-wall-street-journal"
NEWS_LANGUAGE = "en"
MAX_NEWS_ARTICLES = 10

# ==================== CHART SETTINGS ====================

# Color scheme
CHART_COLORS = {
    "primary": "#1f77b4",
    "positive": "#2ecc71",
    "negative": "#e74c3c",
    "neutral": "#95a5a6",
    "accent": "#f39c12"
}

# Chart template
CHART_TEMPLATE = "plotly_white"

# ==================== UI SETTINGS ====================

# Sidebar options
SIDEBAR_OPTIONS = [
    "📊 My Dashboard",
    "📈 Stock Analysis",
    "🔮 Price Prediction",
    "📉 Technical Indicators",
    "💼 Portfolio Tracker",
    "📰 News & Sentiment"
]

# Loading messages
LOADING_MESSAGES = {
    "fetching_data": "Fetching stock data...",
    "analyzing": "Analyzing stock...",
    "predicting": "Generating predictions...",
    "calculating": "Calculating indicators...",
    "loading_news": "Loading latest news..."
}

# ==================== ERROR MESSAGES ====================

ERROR_MESSAGES = {
    "invalid_ticker": "❌ Invalid stock ticker. Please enter a valid symbol.",
    "no_data": "❌ No data available for this stock.",
    "api_error": "❌ Error fetching data. Please try again later.",
    "prediction_error": "❌ Error generating predictions.",
    "portfolio_error": "❌ Error managing portfolio.",
    "news_error": "❌ Error fetching news. Check your API key."
}

# ==================== SUCCESS MESSAGES ====================

SUCCESS_MESSAGES = {
    "data_loaded": "✅ Data loaded successfully!",
    "prediction_complete": "✅ Predictions generated successfully!",
    "portfolio_updated": "✅ Portfolio updated successfully!",
    "stock_added": "✅ Stock added to portfolio!"
}

# ==================== HELPER FUNCTIONS ====================

def get_date_range(period):
    """
    Calculate start and end dates based on period
    
    Args:
        period (str): Time period (e.g., '1y', '6mo')
    
    Returns:
        tuple: (start_date, end_date)
    """
    end_date = datetime.now()
    
    if period == "1mo":
        start_date = end_date - timedelta(days=30)
    elif period == "3mo":
        start_date = end_date - timedelta(days=90)
    elif period == "6mo":
        start_date = end_date - timedelta(days=180)
    elif period == "1y":
        start_date = end_date - timedelta(days=365)
    elif period == "2y":
        start_date = end_date - timedelta(days=730)
    elif period == "5y":
        start_date = end_date - timedelta(days=1825)
    else:  # max
        start_date = end_date - timedelta(days=3650)  # 10 years
    
    return start_date, end_date
