# 📋 Quick Reference Guide

## Common Commands

### Start Application
```bash
streamlit run app.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Update Packages
```bash
pip install --upgrade -r requirements.txt
```

## Stock Ticker Examples

### US Stocks
| Company | Ticker |
|---------|--------|
| Apple | AAPL |
| Microsoft | MSFT |
| Google | GOOGL |
| Amazon | AMZN |
| Tesla | TSLA |
| Meta | META |
| NVIDIA | NVDA |
| JPMorgan | JPM |
| Visa | V |
| Walmart | WMT |

### Indian Stocks (Add .NS)
| Company | Ticker |
|---------|--------|
| Reliance | RELIANCE.NS |
| TCS | TCS.NS |
| Infosys | INFY.NS |
| HDFC Bank | HDFCBANK.NS |
| ICICI Bank | ICICIBANK.NS |
| SBI | SBIN.NS |
| Bharti Airtel | BHARTIARTL.NS |

## Technical Indicators Quick Guide

### RSI (Relative Strength Index)
- **> 70**: Overbought (Consider Selling)
- **< 30**: Oversold (Consider Buying)
- **30-70**: Neutral Zone

### MACD
- **MACD > Signal**: Bullish
- **MACD < Signal**: Bearish
- **Crossover**: Strong signal

### Bollinger Bands
- **Price at Upper Band**: Overbought
- **Price at Lower Band**: Oversold
- **Squeeze**: Low volatility, potential breakout

### Moving Averages
- **Golden Cross**: 50-day MA crosses above 200-day MA (Bullish)
- **Death Cross**: 50-day MA crosses below 200-day MA (Bearish)

## File Structure Reference

### Main Files
- `app.py` - Main application
- `config.py` - Settings and configuration
- `requirements.txt` - Dependencies

### Utils Folder
- `stock_data.py` - Fetch stock data
- `indicators.py` - Technical indicators
- `portfolio.py` - Portfolio management
- `news.py` - News fetching
- `sentiment.py` - Sentiment analysis
- `charts.py` - Chart creation

### Pages Folder
- `home.py` - Home page
- `stock_analysis.py` - Stock analysis
- `prediction.py` - Price prediction
- `technical_indicators.py` - Technical indicators
- `portfolio_tracker.py` - Portfolio tracking
- `news_sentiment.py` - News and sentiment

### Models Folder
- `prediction.py` - ML prediction models

## Keyboard Shortcuts

### In Terminal
- `Ctrl + C` - Stop application
- `Ctrl + D` - Exit Python shell

### In Browser
- `F5` - Refresh page
- `Ctrl + Shift + R` - Hard refresh (clear cache)
- `Ctrl + +/-` - Zoom in/out

## Common Issues & Quick Fixes

### Issue: Module not found
```bash
pip install <module-name>
```

### Issue: Port in use
```bash
streamlit run app.py --server.port 8502
```

### Issue: Cache problems
```bash
streamlit cache clear
```

### Issue: Slow performance
- Use shorter time periods
- Reduce number of indicators
- Close other browser tabs

## API Keys

### NewsAPI
1. Get free key: https://newsapi.org/
2. Edit `config.py`
3. Replace: `NEWS_API_KEY = "your-key"`

## Best Practices

### For Analysis
1. Use 1-2 year data for predictions
2. Combine multiple indicators
3. Check sentiment before trading
4. Diversify portfolio

### For Performance
1. Cache data when possible
2. Use appropriate time periods
3. Close unused pages
4. Clear cache periodically

## Useful Links

- **yfinance Docs**: https://pypi.org/project/yfinance/
- **Streamlit Docs**: https://docs.streamlit.io/
- **Plotly Docs**: https://plotly.com/python/
- **NewsAPI**: https://newsapi.org/docs

## Configuration Options

### In config.py

```python
# Prediction settings
PREDICTION_DAYS = 30  # Days to predict

# Technical indicators
MA_SHORT_PERIOD = 50   # Short MA
MA_LONG_PERIOD = 200   # Long MA
RSI_PERIOD = 14        # RSI period
RSI_OVERBOUGHT = 70    # Overbought level
RSI_OVERSOLD = 30      # Oversold level

# Portfolio
PORTFOLIO_FILE = "data/portfolio.csv"

# News
MAX_NEWS_ARTICLES = 10
```

## Tips & Tricks

1. **Save time**: Use session state to avoid re-fetching
2. **Better predictions**: Use 2+ years of data
3. **News setup**: Get free NewsAPI key
4. **Portfolio**: Export CSV for backup
5. **Charts**: Click legend to hide/show lines

## Performance Tips

- Clear browser cache regularly
- Use recommended time periods
- Limit simultaneous analyses
- Close unused browser tabs
- Restart app if slow

## Troubleshooting Checklist

- [ ] Python 3.8+ installed?
- [ ] Virtual environment activated?
- [ ] Dependencies installed?
- [ ] Internet connection active?
- [ ] Port 8501 available?
- [ ] Valid stock ticker used?
- [ ] Browser cache cleared?

## Support Resources

1. Check error in terminal
2. Review SETUP.md
3. Read README.md
4. Check code comments
5. Verify ticker symbols

---

**Quick Start: `streamlit run app.py`** 🚀
