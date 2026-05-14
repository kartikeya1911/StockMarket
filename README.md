<![CDATA[# 📊 QuantEdge — Stock Market Intelligence Platform

<div align="center">

**AI-powered stock analysis with institutional-grade analytics and explainable recommendations**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.20+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Module Reference](#-module-reference)
- [AI Recommendation Engine](#-ai-recommendation-engine)
- [Machine Learning Pipeline](#-machine-learning-pipeline)
- [Configuration](#-configuration)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [License & Disclaimer](#-license--disclaimer)

---

## 🧭 Overview

**QuantEdge** is a comprehensive, production-ready stock market intelligence platform built with Python and Streamlit. It combines real-time market data, machine learning predictions, 15+ technical indicators, fundamental analysis, news sentiment scoring, and a weighted multi-factor AI recommendation engine — all wrapped in a premium deep-navy dark-mode UI inspired by MoneyControl and Bloomberg Terminal.

### Capabilities

| Feature | Description |
|---|---|
| **AI Recommendation Engine** | Weighted multi-factor scoring (Technical 30% · Fundamental 25% · AI 20% · Sentiment 15% · Risk 10%) |
| **Live Market Indices** | Real-time NIFTY 50, SENSEX, BANK NIFTY, S&P 500, NASDAQ ticker bar |
| **Resilient Data Pipeline** | Triple-fallback fetching (`fast_info` → Quote API → Chart API) with retry/backoff |
| **15+ Technical Indicators** | RSI, MACD, Bollinger, ADX, ATR, OBV, EMA, SMA, Stochastic RSI, Supertrend |
| **Risk Analytics** | Sharpe ratio, Sortino ratio, Max Drawdown, VaR (95%), annualized volatility |
| **Premium UI** | Deep navy + electric cyan palette, glassmorphism cards, JetBrains Mono for data |

---

## ✨ Key Features

### 📊 Dashboard
Real-time portfolio overview with stat cards, holdings table, allocation pie chart, best/worst performers, and per-holding news feed. Live market indices ticker bar at the top.

### 🔍 Stock Analysis
Interactive line & candlestick charts, volume analysis, company fundamentals, 52-week range, historical data export. Supports US, NSE (.NS), and BSE (.BO) tickers.

### 🤖 AI Intelligence Engine
Full 8-step analysis pipeline: data fetch → technical scoring → fundamental scoring → risk analysis → sentiment analysis → ML prediction → support/resistance → weighted recommendation with entry/exit zones, stop-loss, and investment suitability tags.

### 📉 Technical Indicators
RSI, MACD, Bollinger Bands, Moving Averages (50/200 SMA, 20 EMA) with automated trading signal generation and interactive Plotly charts.

### 🔮 Price Prediction
ML-powered 30-day forecasts using Linear Regression or Random Forest with rolling-window feature updates, confidence scoring, and feature importance analysis.

### 💼 Portfolio Tracker
Add/remove stocks with automatic weighted-average cost basis calculation, real-time P&L, allocation charts, risk assessment, and CSV persistence.

### 📰 News & Sentiment
NewsAPI integration with TextBlob sentiment analysis, sentiment distribution charts, and market outlook recommendations.

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                          │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌────────────────┐  │
│  │ Dashboard  │ │ Stock     │ │ AI Intel  │ │ Technical      │  │
│  │           │ │ Analysis  │ │ Engine    │ │ Indicators     │  │
│  └───────────┘ └───────────┘ └───────────┘ └────────────────┘  │
│  ┌───────────┐ ┌───────────┐ ┌──────────────────────────────┐  │
│  │ Prediction│ │ Portfolio │ │ News & Sentiment             │  │
│  └───────────┘ └───────────┘ └──────────────────────────────┘  │
│                    pages/*.py  +  styles/theme.py                │
├──────────────────────────────────────────────────────────────────┤
│                        SERVICE LAYER                             │
│  ┌─────────────────────────┐  ┌─────────────────────────────┐   │
│  │  Analysis Engine        │  │  Recommendation Engine      │   │
│  │  • Technical Scoring    │  │  • Multi-Factor Weighting   │   │
│  │  • Fundamental Scoring  │──│  • Explainable AI Reasoning │   │
│  │  • Risk Scoring         │  │  • Entry/Exit/Stop-Loss     │   │
│  └─────────────────────────┘  └─────────────────────────────┘   │
│                       services/*.py                              │
├──────────────────────────────────────────────────────────────────┤
│                        CORE LAYER                                │
│  ┌────────────┐ ┌──────────┐ ┌─────────┐ ┌─────────┐ ┌──────┐  │
│  │StockData   │ │Technical │ │Portfolio│ │News     │ │Senti │  │
│  │Fetcher     │ │Indicators│ │Manager  │ │Fetcher  │ │ment  │  │
│  │(3-fallback)│ │(ta lib)  │ │(CSV)    │ │(NewsAPI)│ │(Blob)│  │
│  └────────────┘ └──────────┘ └─────────┘ └─────────┘ └──────┘  │
│  ┌────────────┐ ┌──────────────────────────────────────────────┐│
│  │ML Models   │ │Charts (Plotly dark theme)                    ││
│  │(sklearn)   │ │Line, Candlestick, Radar, Gauge, Pie, MACD   ││
│  └────────────┘ └──────────────────────────────────────────────┘│
│              utils/*.py  +  models/*.py                          │
├──────────────────────────────────────────────────────────────────┤
│                     EXTERNAL DATA SOURCES                        │
│  ┌────────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │ Yahoo Finance  │  │  NewsAPI.org  │  │  CSV Storage         │ │
│  │ (yfinance +    │  │  (REST API)   │  │  (data/portfolio.csv)│ │
│  │  REST fallback)│  │              │  │                      │ │
│  └────────────────┘  └──────────────┘  └──────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
StockMarket/
├── app.py                         # Entry point — sidebar, market ticker, routing
├── config.py                      # Centralized settings (ML, indicators, UI, API)
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── QUICKREF.md                    # Quick reference guide
├── MODELS_DOCUMENTATION.md        # ML models deep-dive
├── .env.example                   # Environment variable template
│
├── .streamlit/
│   └── config.toml                # Theme (deep navy #0A0E27, cyan #00D4FF)
│
├── pages/                         # Streamlit multi-page UI
│   ├── dashboard.py               # Portfolio dashboard with market ticker
│   ├── stock_analysis.py          # Stock analysis with charts
│   ├── ai_intelligence.py         # AI recommendation engine (8-step)
│   ├── technical_indicators.py    # RSI, MACD, Bollinger, MA
│   ├── prediction.py              # ML price prediction
│   ├── portfolio_tracker.py       # Portfolio CRUD
│   └── news_sentiment.py          # News + sentiment scoring
│
├── services/                      # Business logic
│   ├── analysis_engine.py         # Technical, fundamental, risk scoring
│   └── recommendation_engine.py   # Weighted AI recommendation
│
├── models/                        # Machine learning
│   └── prediction.py              # StockPredictor (LR, RF, rolling)
│
├── utils/                         # Core utilities
│   ├── stock_data.py              # StockDataFetcher (3-fallback)
│   ├── indicators.py              # TechnicalIndicators (ta wrappers)
│   ├── portfolio.py               # PortfolioManager (CSV CRUD)
│   ├── news.py                    # NewsFetcher (NewsAPI)
│   ├── sentiment.py               # SentimentAnalyzer (TextBlob)
│   └── charts.py                  # Plotly chart builders
│
├── styles/                        # UI theme
│   └── theme.py                   # Premium CSS + component helpers
│
└── data/                          # Runtime data
    └── portfolio.csv              # Portfolio persistence
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Streamlit ≥1.35 | Multi-page web application |
| **Styling** | Custom CSS | Deep navy glassmorphism, Inter + JetBrains Mono |
| **Data** | yfinance ≥0.2.38 | Yahoo Finance (OHLCV, fundamentals) |
| **ML** | scikit-learn ≥1.4, XGBoost ≥2.0 | Prediction models |
| **Indicators** | ta ≥0.11 | RSI, MACD, Bollinger, SMA, EMA |
| **Visualization** | Plotly ≥5.20 | Interactive dark-themed charts |
| **NLP** | TextBlob ≥0.18 | Sentiment analysis |
| **News** | newsapi-python ≥0.2.7 | Financial news aggregation |
| **Data** | pandas ≥2.2, numpy ≥1.26 | DataFrames, numerical computation |

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/kartikeya1911/StockMarket.git
cd StockMarket

# 2. Virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# 3. Install
pip install -r requirements.txt

# 4. (Optional) News API
cp .env.example .env
# Set NEWS_API_KEY=your_key_from_newsapi.org

# 5. Run
streamlit run app.py
```

Opens at `http://localhost:8501`.

---

## 📦 Module Reference

### `services/analysis_engine.py`

| Function | Output |
|---|---|
| `compute_technical_score(data, price)` | Score 0-100 + signals (RSI, MACD, MA, BB, ADX, OBV, ATR) |
| `compute_fundamental_score(info)` | Score 0-100 + metrics (PE, PB, ROE, D/E, Beta, EPS) |
| `compute_risk_score(data)` | Score 0-100 + Sharpe, Sortino, Max DD, VaR(95%) |
| `compute_support_resistance(data)` | Pivot, S1/S2, R1/R2, Fibonacci levels |

### `services/recommendation_engine.py`

Combines all scores with configurable weights. Outputs: recommendation, composite score, confidence, 5 explainable reasons, entry/exit zones, stop-loss, suitability tags.

### `models/prediction.py`

| Model | Config | Best For |
|---|---|---|
| Linear Regression | Default sklearn | Linear trends, fast inference |
| Random Forest | 100 trees, depth=10 | Non-linear patterns, feature importance |

### `utils/stock_data.py` — StockDataFetcher

Triple-fallback: `fast_info` → Quote REST API → Chart REST API. Each with 6 retries, exponential backoff, handles 401/429/5xx.

---

## 🤖 AI Recommendation Engine

### Weights

```python
RECOMMENDATION_WEIGHTS = {
    "technical":     0.30,   # RSI, MACD, MA, Bollinger, ADX, OBV
    "fundamental":   0.25,   # PE, PB, ROE, D/E, Beta, EPS, Dividend
    "ai_prediction": 0.20,   # 30-day Random Forest forecast
    "sentiment":     0.15,   # TextBlob polarity from news
    "risk":          0.10,   # Volatility, Sharpe, Sortino, Drawdown
}
```

### Scoring

| Score | Recommendation |
|---|---|
| ≥ 80 | **Strong Buy** |
| ≥ 60 | **Buy** |
| ≥ 40 | **Hold** |
| ≥ 20 | **Sell** |
| < 20 | **Strong Sell** |

---

## 🧠 Machine Learning Pipeline

```
Historical OHLCV → Feature Engineering → Train/Test Split (80/20)
→ Model Training → Evaluation (R², RMSE, MAE)
→ 30-Day Rolling Prediction → Confidence Assessment
```

**Features:** Days, OHLCV, MA_5/10/20, Volatility, Returns, Day/Month
**Rolling prediction** updates MAs each step to prevent flat-line forecasts.

---

## ⚙️ Configuration

All settings in `config.py`. Key parameters:

| Setting | Value | Description |
|---|---|---|
| `PREDICTION_DAYS` | 30 | Forecast horizon |
| `RSI_PERIOD` | 14 | RSI calculation window |
| `MACD_FAST/SLOW/SIGNAL` | 12/26/9 | MACD periods |
| `BB_PERIOD` / `BB_STD_DEV` | 20 / 2 | Bollinger Bands |
| `TRAIN_TEST_SPLIT` | 0.8 | ML train/test ratio |

### Supported Tickers

| Market | Format | Examples |
|---|---|---|
| US | `TICKER` | AAPL, MSFT, GOOGL, TSLA |
| India (NSE) | `TICKER.NS` | RELIANCE.NS, TCS.NS, INFY.NS |
| India (BSE) | `TICKER.BO` | RELIANCE.BO, TCS.BO |

---

## 📚 API Reference

```python
from utils.stock_data import StockDataFetcher
fetcher = StockDataFetcher("RELIANCE.NS")
fetcher.validate_ticker()               # → True/False
fetcher.get_stock_info()                # → dict (15+ fields)
fetcher.get_historical_data("1y")       # → DataFrame (OHLCV)
fetcher.get_realtime_price()            # → dict (price, change, %)

from services.recommendation_engine import generate_recommendation
rec = generate_recommendation(tech, fund, sent, pred, risk, price, sr)
# rec['recommendation']  → "Strong Buy" / "Buy" / "Hold" / ...
# rec['composite_score'] → 0-100
# rec['confidence']      → 0-100
# rec['reasons']         → list of 5 explanations
```

---

## ⚠️ Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| "No data available" | Add `.NS` for NSE stocks |
| News not loading | Set `NEWS_API_KEY` in `.env` |
| Yahoo 429/401 errors | Built-in backoff handles this automatically |
| Portfolio not saving | `data/` directory auto-created on startup |
| Flat predictions | Fixed — rolling-window MAs prevent this |

---

## 📄 License & Disclaimer

Open source under the **MIT License**.

> **⚠️ Disclaimer:** For **educational and informational purposes only**. NOT financial advice. Always consult a qualified financial advisor before making investment decisions.

---

<div align="center">

**Built with ❤️ using Python, Streamlit & scikit-learn**

📊 **QuantEdge v4.0.0** 📊

</div>
]]>
