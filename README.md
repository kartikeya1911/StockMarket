# 📈 Stock Market Analysis & Prediction Web Application

A comprehensive, production-ready stock market analysis platform built with Python and Streamlit. This application provides real-time data analysis, machine learning-based predictions, technical indicators, portfolio management, and news sentiment analysis.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 📊 Stock Analysis Dashboard
- Real-time stock data fetching using yfinance
- Interactive price charts (line and candlestick)
- Trading volume analysis
- Company information and key metrics
- Historical data tables with export functionality

### 🔮 AI-Powered Price Prediction
- Machine Learning models (Linear Regression & Random Forest)
- 30-day price forecasts
- Model performance metrics (R², RMSE, MAE)
- Confidence level indicators
- Visual prediction charts

### 📈 Technical Indicators
- **RSI** (Relative Strength Index) with overbought/oversold signals
- **MACD** (Moving Average Convergence Divergence)
- **Bollinger Bands** with price position analysis
- **Moving Averages** (50-day and 200-day SMA)
- Automated trading signals and recommendations

### 💼 Portfolio Tracker
- Add and manage multiple stocks
- Real-time profit/loss calculation
- Portfolio allocation visualization
- Best and worst performer identification
- Risk assessment and diversification metrics
- Export portfolio reports

### 📰 News & Sentiment Analysis
- Latest stock news aggregation
- AI-powered sentiment analysis using TextBlob
- Sentiment distribution charts
- Market outlook recommendations
- Individual article sentiment scores

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   cd StockMarket
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   The application will automatically open at `http://localhost:8501`

## 📁 Project Structure

```
StockMarket/
│
├── app.py                      # Main application entry point
├── config.py                   # Configuration and settings
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── data/                       # Data storage directory
│   └── portfolio.csv          # Portfolio data (auto-created)
│
├── models/                     # Machine learning models
│   ├── __init__.py
│   └── prediction.py          # Price prediction models
│
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── stock_data.py          # Stock data fetching
│   ├── indicators.py          # Technical indicators
│   ├── portfolio.py           # Portfolio management
│   ├── news.py                # News fetching
│   ├── sentiment.py           # Sentiment analysis
│   └── charts.py              # Chart creation
│
└── pages/                      # Application pages
    ├── __init__.py
    ├── home.py                # Home page
    ├── stock_analysis.py      # Stock analysis page
    ├── prediction.py          # Prediction page
    ├── technical_indicators.py # Technical indicators page
    ├── portfolio_tracker.py   # Portfolio page
    └── news_sentiment.py      # News & sentiment page
```

## 📖 Usage Guide

### Stock Analysis
1. Navigate to "📊 Stock Analysis"
2. Enter a stock ticker (e.g., AAPL, TSLA, RELIANCE.NS)
3. Select time period and interval
4. Click "Analyze Stock"
5. View charts, metrics, and historical data

### Price Prediction
1. Navigate to "🔮 Price Prediction"
2. Enter stock ticker
3. Choose model type (Linear Regression or Random Forest)
4. Select training period
5. Click "Generate Prediction"
6. Review predictions and model accuracy

### Technical Indicators
1. Navigate to "📈 Technical Indicators"
2. Enter stock ticker
3. Select time period
4. Click "Analyze Indicators"
5. Review signals and trading recommendations

### Portfolio Management
1. Navigate to "💼 Portfolio Tracker"
2. Use sidebar to add stocks
3. Enter quantity, purchase price, and date
4. View portfolio performance and allocation
5. Track profit/loss in real-time

### News & Sentiment
1. Navigate to "📰 News & Sentiment"
2. Enter stock ticker
3. Select news period
4. Click "Fetch News"
5. Review sentiment analysis and recommendations

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

- **Frontend:** Streamlit
- **Data:** yfinance, pandas, numpy
- **Visualization:** Plotly
- **Machine Learning:** scikit-learn
- **Technical Analysis:** ta (Technical Analysis library)
- **NLP:** TextBlob
- **News:** NewsAPI

## 📊 Key Features Details

### Machine Learning Models
- **Linear Regression:** Fast, baseline model for trend prediction
- **Random Forest:** More complex ensemble model for better accuracy
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

### Future Enhancements
- [ ] Add more ML models (LSTM, Prophet)
- [ ] Implement backtesting functionality
- [ ] Add cryptocurrency support
- [ ] Create mobile-responsive design
- [ ] Add user authentication
- [ ] Implement database storage
- [ ] Add email alerts

## 📧 Support

For issues, questions, or suggestions:
- Check existing documentation
- Review code comments
- Test with popular stock tickers first

## 🌟 Acknowledgments

- **yfinance** for stock data
- **Streamlit** for the amazing framework
- **Plotly** for interactive charts
- **scikit-learn** for ML capabilities

---

**Made with ❤️ using Python and Streamlit**

*Happy Trading! 📈*
