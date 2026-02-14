# 📈 Stock Market Analysis & Portfolio Management Platform

A comprehensive, production-ready stock market analysis platform built with Python and Streamlit. This application provides real-time data analysis, machine learning-based predictions, technical indicators, intelligent portfolio management with automatic averaging, and news aggregation for your holdings.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📑 Table of Contents
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Usage Guide](#-usage-guide)
- [Configuration](#-configuration)
- [Technical Details](#-technical-details)
- [API Documentation](#-api-documentation)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## ✨ Features

### 📊 Portfolio Dashboard
- **Real-time Portfolio Overview** - Track total investment vs current value
- **Holdings Management** - View all your stock holdings in one place
- **Performance Analytics** - Best and worst performers
- **Portfolio Allocation Chart** - Visual representation of your investments
- **Latest News Feed** - One news article per holding automatically fetched
- **Delete Functionality** - Easy stock removal with one click

### 📈 Stock Analysis
- Real-time stock data fetching using yfinance
- Interactive price charts (line and candlestick)
- Trading volume analysis
- Company information and key metrics
- Historical data tables with export functionality
- Support for US stocks and Indian stocks (NSE/BSE)

### 🔮 AI-Powered Price Prediction
- **Machine Learning Models:**
  - Linear Regression for baseline predictions
  - Random Forest for complex pattern recognition
- 30-day price forecasts with proper trend analysis
- Model performance metrics (R², RMSE, MAE)
- Confidence level indicators
- Visual prediction charts with historical context
- **Fixed** - No more horizontal line predictions!

### 📉 Technical Indicators
- **RSI** (Relative Strength Index) with overbought/oversold signals
- **MACD** (Moving Average Convergence Divergence)
- **Bollinger Bands** with price position analysis
- **Moving Averages** (50-day and 200-day SMA)
- Automated trading signals and recommendations

### 💼 Smart Portfolio Tracker
- **Add Stocks** - Simple form to add stocks to your portfolio
- **Automatic Averaging** - When you buy the same stock twice:
  - Quantities are added together
  - Purchase prices are weighted-averaged
  - Single entry per stock maintained
- **Real-time P&L** - Live profit/loss calculation
- **Portfolio Metrics** - Diversification and risk assessment
- **Best & Worst Performers** - Instant identification
- **One-Click Removal** - Delete stocks with 🗑️ button
- **Latest News** - Automatic news fetching for each holding

### 📰 News & Sentiment Analysis
- Latest stock news aggregation using NewsAPI
- AI-powered sentiment analysis using TextBlob
- Sentiment distribution charts
- Market outlook recommendations
- Individual article sentiment scores
- **Smart Ticker Handling** - Automatically handles .NS, .BO suffixes

## 🚀 Quick Start

### Prerequisites
- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** (Python package manager) - Usually comes with Python
- **Internet connection** - For fetching real-time stock data

### Installation

1. **Clone or download the project**
   ```bash
   git clone https://github.com/kartikeya1911/StockMarket.git
   cd StockMarket
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   
   # Activate on Windows
   .venv\Scripts\activate
   
   # Activate on macOS/Linux
   source .venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Configure News API**
   - Get a free API key from [NewsAPI.org](https://newsapi.org/)
   - Open `config.py`
   - Replace `NEWS_API_KEY` with your API key
   - If you skip this, sample news will be displayed

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the application**
   - The app will automatically open in your browser
   - Or manually navigate to `http://localhost:8501`

### First Time Setup

1. **Go to Portfolio Tracker** page
2. **Add your first stock** using the form at the top:
   - Enter ticker symbol (e.g., AAPL, RELIANCE.NS)
   - Enter quantity and purchase price
   - Select purchase date
   - Click "Add to Portfolio"
3. **View Dashboard** to see your portfolio overview

## 📁 Project Structure

```
StockMarket/
│
├── app.py                      # Main application entry point & routing
├── config.py                   # Configuration settings & constants
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation (this file)
├── SETUP.md                    # Detailed setup instructions
├── QUICKREF.md                 # Quick reference guide
│
├── data/                       # Data storage directory
│   ├── .gitkeep               # Keeps folder in git
│   └── portfolio.csv          # Portfolio data (auto-created)
│
├── models/                     # Machine learning models
│   ├── __init__.py
│   └── prediction.py          # Price prediction algorithms
│
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── stock_data.py          # Stock data fetching (yfinance)
│   ├── indicators.py          # Technical indicators calculation
│   ├── portfolio.py           # Portfolio management logic
│   ├── news.py                # News fetching (NewsAPI)
│   ├── sentiment.py           # Sentiment analysis (TextBlob)
│   └── charts.py              # Chart creation (Plotly)
│
└── pages/                      # Application pages (Streamlit multipage)
    ├── __init__.py
    ├── dashboard.py           # Portfolio dashboard (default page)
    ├── stock_analysis.py      # Stock analysis tools
    ├── prediction.py          # ML price prediction
    ├── technical_indicators.py # Technical analysis
    ├── portfolio_tracker.py   # Portfolio management
    └── news_sentiment.py      # News & sentiment analysis
```
    ├── home.py                # Home page
    ├── stock_analysis.py      # Stock analysis page
    ├── prediction.py          # Prediction page
    ├── technical_indicators.py # Technical indicators page
    ├── portfolio_tracker.py   # Portfolio page
    └── news_sentiment.py      # News & sentiment page
```

## 📖 Usage Guide

### 📊 Dashboard (Landing Page)
Your portfolio overview opens by default when you start the app.

**What you'll see:**
- 💰 Total Investment (highlighted in purple gradient)
- 💵 Current Value (highlighted in green gradient)
- 📈 Total Gain/Loss with percentage
- 🏢 Number of holdings
- 📋 Holdings table with all stocks
- 📊 Portfolio allocation pie chart
- 🏆 Best and worst performers
- 📰 Latest news for each stock (collapsed by default)

**Actions you can take:**
- Click 🗑️ button to remove any stock
- Expand news sections to read latest articles

### 💼 Portfolio Tracker
Manage your stock portfolio with ease.

**Adding Stocks:**
1. Fill in the form at the top:
   - **Ticker Symbol**: Enter stock ticker (AAPL, RELIANCE.NS, etc.)
   - **Quantity**: Number of shares
   - **Purchase Price**: Price per share at purchase
   - **Purchase Date**: Date of purchase
2. Click "Add to Portfolio"

**Automatic Averaging Feature:**
- If you buy the same stock multiple times, the system automatically:
  - Adds quantities together
  - Calculates weighted average purchase price
  - Maintains only one entry per stock
  - Example: 10 shares @ $100 + 5 shares @ $130 = 15 shares @ $110 avg

**View Your Holdings:**
- See detailed table with buy price, current price, gains/losses
- Portfolio allocation chart
- Performance metrics
- Latest news for each holding
- Risk assessment

**Remove Stocks:**
- Click the 🗑️ button next to any stock to remove it

### 📈 Stock Analysis
Analyze any stock with comprehensive data and charts.

1. Navigate to "📈 Stock Analysis"
2. Enter stock ticker (e.g., AAPL, TSLA, RELIANCE.NS for Indian stocks)
3. Select time period (1M, 3M, 6M, 1Y, 2Y, 5Y, Max)
4. Select interval (1 Day, 1 Week, 1 Month)
5. Click "Analyze Stock"

**You'll see:**
- Line chart and candlestick chart
- Current price, market cap, PE ratio
- 52-week high/low
- Trading volume chart
- Historical data table (exportable)

### 🔮 Price Prediction
AI-powered price forecasts using machine learning.

1. Navigate to "🔮 Price Prediction"
2. Enter stock ticker
3. Choose model:
   - **Linear Regression**: Fast, good for linear trends
   - **Random Forest**: Better for complex patterns
4. Select training period (1Y, 2Y, 5Y)
5. Click "Generate Prediction"

**Results include:**
- Model accuracy metrics (R², RMSE, MAE)
- Confidence level (High/Moderate/Low)
- 30-day prediction chart
- 7-day and 30-day price predictions
- Detailed predictions table

**Note:** Predictions are based on historical data and technical indicators. Not financial advice!

### 📉 Technical Indicators
Advanced technical analysis with trading signals.

1. Navigate to "📉 Technical Indicators"
2. Enter stock ticker
3. Select time period
4. Click "Analyze Indicators"

**Indicators included:**
- **RSI (14)**: Overbought (>70) / Oversold (<30) signals
- **MACD**: Trend direction and momentum
- **Bollinger Bands**: Volatility and potential breakouts
- **Moving Averages**: 50-day and 200-day SMA
  - Golden Cross (bullish) / Death Cross (bearish)

**Trading Signals:**
- Buy/Sell/Hold recommendations
- Signal strength indicators
- Visual charts for each indicator

### 📰 News & Sentiment
Get latest news with AI-powered sentiment analysis.

1. Navigate to "📰 News & Sentiment"
2. Enter stock ticker
3. Select news period (1-7 days)
4. Click "Fetch News"

**Features:**
- Latest news articles from multiple sources
- Sentiment analysis (Positive/Neutral/Negative)
- Sentiment distribution chart
- Overall market outlook
- Clickable article links

**Note:** Requires NewsAPI key for real-time news. Without it, sample news is shown.

## 🔧 Configuration

### News API Setup (Optional)
To get real-time news, obtain a free API key:

1. Visit [https://newsapi.org/](https://newsapi.org/)
2. Sign up for a free account
3. Copy your API key
4. Open `config.py`
5. Replace `YOUR_API_KEY_HERE` with your API key
6. Restart the application

Without an API key, the app will show sample news data.

### Stock Ticker Examples

**US Stocks:**
- AAPL (Apple)
- MSFT (Microsoft)
- GOOGL (Google)
- TSLA (Tesla)
- AMZN (Amazon)

**Indian Stocks (add .NS suffix):**
- RELIANCE.NS
- TCS.NS
- INFY.NS
- HDFCBANK.NS

## 🛠️ Technologies Used

- **Frontend Framework:** Streamlit 1.32.0
- **Data Fetching:** yfinance (Yahoo Finance API)
- **Data Processing:** pandas, numpy
- **Visualization:** Plotly (interactive charts)
- **Machine Learning:** scikit-learn (Linear Regression, Random Forest)
- **Technical Analysis:** ta library
- **Natural Language Processing:** TextBlob
- **News API:** NewsAPI
- **Python Version:** 3.8+

## 📊 Technical Details

### Machine Learning Models

**Linear Regression:**
- Fast training and prediction
- Good for stocks with linear trends
- Baseline model for comparison
- Features: Days, OHLCV, moving averages, volatility, returns

**Random Forest:**
- Ensemble of decision trees
- Handles non-linear patterns
- Better accuracy for complex stocks
- Provides feature importance
- Parameters: 100 trees, max depth 10

**Feature Engineering:**
- Days (sequential numbering)
- OHLCV (Open, High, Low, Close, Volume)
- Moving Averages (5, 10, 20-day)
- Volatility (10-day standard deviation)
- Daily Returns (percentage changes)
- Day of week and month (when available)

**Prediction Process:**
1. Prepare historical data with technical features
2. Split data (80% training, 20% testing)
3. Train model on training set
4. Validate on test set
5. Generate 30-day future predictions
6. Use rolling window for realistic predictions (no horizontal lines!)

### Portfolio Management Logic

**Add Stock:**
- Validates ticker using yfinance
- Fetches company name
- Checks if stock already exists
- If exists: Averages purchase price and adds quantity
- If new: Creates new entry
- Formula: `Avg Price = (Old Investment + New Investment) / Total Quantity`

**Remove Stock:**
- Removes by ticker symbol
- Updates portfolio.csv
- No confirmation prompt (direct removal)

**P&L Calculation:**
- Fetches real-time price from yfinance
- Calculates: `Gain/Loss = (Current Price - Purchase Price) × Quantity`
- Percentage: `(Gain/Loss / Investment) × 100`

**Portfolio Metrics:**
- Number of holdings
- Weighted average gain
- Maximum allocation percentage
- Risk level (High/Moderate/Low based on concentration)

### News Fetching Logic

**Ticker Normalization:**
- Strips exchange suffixes (.NS, .BO, etc.)
- Example: RELIANCE.NS → RELIANCE
- Fetches company name for better search results
- Example: ONGC.NS → "Oil and Natural Gas Corporation"

**API Integration:**
- Uses NewsAPI for real-time news
- Falls back to sample news if API key missing
- Searches by company name (not ticker)
- Caches results for 30 minutes
- Returns most recent articles first

## 🔧 Configuration

### config.py Settings

```python
# Prediction settings
PREDICTION_DAYS = 30          # Days to predict into future
TRAIN_TEST_SPLIT = 0.8        # 80% training, 20% testing

# Technical indicators
RSI_PERIOD = 14               # RSI calculation period
RSI_OVERBOUGHT = 70           # RSI overbought threshold
RSI_OVERSOLD = 30             # RSI oversold threshold
MACD_FAST = 12                # MACD fast period
MACD_SLOW = 26                # MACD slow period
MACD_SIGNAL = 9               # MACD signal period

# Portfolio
PORTFOLIO_FILE = "data/portfolio.csv"

# News API
NEWS_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your key
```

### News API Setup

1. **Get Free API Key:**
   - Visit [https://newsapi.org/](https://newsapi.org/)
   - Sign up for free account (500 requests/day)
   - Copy your API key

2. **Configure:**
   - Open `config.py`
   - Find `NEWS_API_KEY = "YOUR_API_KEY_HERE"`
   - Replace with your actual key
   - Save file

3. **Restart Application:**
   ```bash
   streamlit run app.py
   ```

### Stock Ticker Format

**US Stocks:**
- Format: `TICKER`
- Examples: AAPL, MSFT, GOOGL, TSLA, AMZN

**Indian Stocks (NSE):**
- Format: `TICKER.NS`
- Examples: RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS

**Indian Stocks (BSE):**
- Format: `TICKER.BO`
- Examples: RELIANCE.BO, TCS.BO

## ⚠️ Troubleshooting

### Common Issues

**1. Module Not Found Error**
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution:** Install requirements
```bash
pip install -r requirements.txt
```

**2. No Data for Stock**
```
❌ No data available for this stock.
```
**Solution:**
- Check ticker symbol is correct
- Add .NS for Indian NSE stocks
- Add .BO for Indian BSE stocks
- Some stocks may not have historical data

**3. News Not Fetching**
```
Unable to fetch news
```
**Solution:**
- News API key not configured (sample news will show)
- Or get free API key from newsapi.org
- Check internet connection

**4. Prediction Shows Horizontal Line**
**Solution:** Already fixed in latest version! The predict_future() function now properly calculates rolling moving averages.

**5. Portfolio Not Saving**
```
Error saving portfolio
```
**Solution:**
- Check `data/` folder exists
- Check file permissions
- Manually create `data/` folder if missing

**6. Duplicate Key Error**
```
StreamlitDuplicateElementKey
```
**Solution:** Already fixed! Each button now has unique index-based keys.

### Performance Tips

1. **Slow Predictions?**
   - Use shorter training period (1Y instead of 5Y)
   - Use Linear Regression instead of Random Forest
   - Random Forest takes longer but is more accurate

2. **Slow Data Loading?**
   - yfinance fetches from Yahoo Finance servers
   - May be slow during high traffic
   - Try shorter time periods

3. **App Not Responding?**
   - Press Ctrl+C in terminal to stop
   - Restart: `streamlit run app.py`
   - Clear cache: Click "Clear Cache" in Streamlit menu

## 📚 API Documentation

### StockDataFetcher (utils/stock_data.py)

```python
from utils.stock_data import StockDataFetcher

# Initialize
fetcher = StockDataFetcher("AAPL")

# Validate ticker
is_valid = fetcher.validate_ticker()

# Get stock info
info = fetcher.get_stock_info()
# Returns: {name, current_price, previous_close, market_cap, pe_ratio, ...}

# Get historical data
data = fetcher.get_historical_data(period="1y", interval="1d")
# Returns: DataFrame with Date, Open, High, Low, Close, Volume

# Get real-time price
price = fetcher.get_realtime_price()
# Returns: {current_price, previous_close, change, change_percent}
```

### PortfolioManager (utils/portfolio.py)

```python
from utils.portfolio import PortfolioManager

# Initialize
pm = PortfolioManager()

# Add stock (auto-averages if exists)
pm.add_stock("AAPL", quantity=10, purchase_price=150.0, purchase_date="2024-01-01")

# Remove stock
pm.remove_stock("AAPL")

# Get portfolio summary
summary = pm.get_portfolio_summary()
# Returns: {total_stocks, total_investment, current_value, total_gain_loss, ...}

# Get allocation
allocation = pm.get_portfolio_allocation()

# Get best/worst performers
performers = pm.get_best_worst_performers()
```

### NewsFetcher (utils/news.py)

```python
from utils.news import NewsFetcher

# Initialize
nf = NewsFetcher()

# Fetch news (auto-handles .NS suffix)
articles = nf.fetch_stock_news("RELIANCE.NS", days_back=7, max_articles=10)
# Returns: List of {title, description, url, publishedAt, source}
```

### Prediction (models/prediction.py)

```python
from models.prediction import create_prediction_pipeline

# Create prediction pipeline
predictor, metrics, predictions = create_prediction_pipeline(
    historical_data, 
    model_type='random_forest'  # or 'linear'
)

# metrics contains: train_rmse, test_rmse, train_r2, test_r2, etc.
# predictions: DataFrame with Date, Predicted_Close
```
- **Feature Engineering:** Includes moving averages, volatility, and returns
- **Model Evaluation:** R² score, RMSE, and MAE metrics

### Technical Indicators Explained
- **RSI:** Measures momentum, identifies overbought (>70) and oversold (<30) conditions
- **MACD:** Shows trend direction and momentum through moving average convergence
- **Bollinger Bands:** Displays volatility and potential price breakouts
- **Moving Averages:** Identifies trend direction (Golden Cross/Death Cross)

## ⚠️ Disclaimer

This application is for **educational and informational purposes only**. It should NOT be considered as financial advice. 

- Stock market predictions are based on historical data and may not reflect future performance
- Always conduct your own research
- Consult with qualified financial advisors before making investment decisions
- Past performance does not guarantee future results

## 🤝 Contributing

This is an educational project. Feel free to:
- Fork the repository
- Add new features
- Improve existing functionality
- Report bugs
- Suggest enhancements

## 📝 License

This project is provided as-is for educational purposes.

## 👨‍💻 Developer Notes

### Code Structure
- **Modular design:** Each feature in separate files
- **Clean code:** Well-commented and documented
- **Scalable:** Easy to add new features
- **Professional:** Production-ready code quality

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Issues
1. Check if issue already exists
2. Provide detailed description
3. Include error messages and screenshots
4. Mention Python and package versions

### Suggesting Enhancements
1. Open an issue with "[FEATURE]" prefix
2. Describe the feature and use case
3. Explain expected behavior

### Code Contributions
1. Fork the repository
2. Create feature branch: `git checkout -b feature/YourFeature`
3. Make changes with clear comments
4. Test thoroughly
5. Commit: `git commit -m "Add YourFeature"`
6. Push: `git push origin feature/YourFeature`
7. Open Pull Request with description

### Code Style Guidelines
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic
- Keep functions focused and small

### Testing Checklist
- [ ] Test with US stocks (AAPL, MSFT)
- [ ] Test with Indian stocks (.NS suffix)
- [ ] Verify portfolio add/remove/average
- [ ] Check predictions show trends (not flat)
- [ ] Ensure news fetches correctly
- [ ] Test all technical indicators
- [ ] Verify sentiment analysis

## 🔮 Future Enhancements

**Machine Learning:**
- [ ] LSTM neural networks for time series
- [ ] Prophet model for seasonal patterns
- [ ] Ensemble voting from multiple models
- [ ] Real-time model retraining

**Portfolio Features:**
- [ ] Dividend tracking
- [ ] Tax calculation (capital gains)
- [ ] Portfolio rebalancing suggestions
- [ ] Risk-adjusted returns (Sharpe ratio)
- [ ] Historical performance charts

**Data & Analysis:**
- [ ] Cryptocurrency support (Bitcoin, Ethereum)
- [ ] Forex pairs analysis
- [ ] Fundamental analysis (P/E, debt ratios)
- [ ] Comparison with market indices
- [ ] Correlation matrix between holdings

**Technical Features:**
- [ ] User authentication & multi-user support
- [ ] Database storage (SQLite/PostgreSQL)
- [ ] Export to Excel/PDF reports
- [ ] Email/SMS alerts for price targets
- [ ] Mobile-responsive design
- [ ] Dark mode theme

**Trading Features:**
- [ ] Backtesting strategies
- [ ] Paper trading simulator
- [ ] Stop-loss/take-profit recommendations
- [ ] Options pricing calculator
- [ ] Screener for finding stocks

## 📄 License

This project is open source and available for educational purposes.

**Disclaimer:** This application is for educational and informational purposes only. It is not financial advice. Always do your own research and consult with a qualified financial advisor before making investment decisions. Past performance does not guarantee future results.

## 🙏 Acknowledgments

**Built With:**
- [Streamlit](https://streamlit.io/) - Amazing Python web framework
- [yfinance](https://github.com/ranaroussi/yfinance) - Yahoo Finance data API
- [Plotly](https://plotly.com/) - Interactive visualization library
- [scikit-learn](https://scikit-learn.org/) - Machine learning toolkit
- [TA-Lib](https://github.com/bukosabino/ta) - Technical analysis library
- [TextBlob](https://textblob.readthedocs.io/) - NLP and sentiment analysis
- [NewsAPI](https://newsapi.org/) - News aggregation service

**Special Thanks:**
- Yahoo Finance for providing free financial data
- The open-source community for amazing libraries
- Streamlit team for their excellent framework
- Contributors and users of this project

## 📞 Contact & Support

**For Issues:**
- Check [Troubleshooting](#️-troubleshooting) section first
- Review code comments and documentation
- Test with known working stocks (AAPL, MSFT)

**For Questions:**
- Read the Usage Guide section
- Check API Documentation
- Review Configuration settings

**For Feature Requests:**
- Open an issue with detailed description
- Explain the use case and benefits
- Check Future Enhancements section

---

<div align="center">

**Made with ❤️ using Python and Streamlit**

📈 **Happy Trading & Investing!** 📊

*Remember: This is for educational purposes. Always do your own research!*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red)]()
[![yfinance](https://img.shields.io/badge/yfinance-latest-green)]()

</div>
