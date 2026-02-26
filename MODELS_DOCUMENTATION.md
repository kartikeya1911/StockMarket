# Machine Learning Models & Techniques Documentation

## Overview
This document outlines all the machine learning models, algorithms, and analytical techniques used in the StockMarket application.

---

## 1. Predictive Models

### 1.1 Linear Regression
**Purpose:** Stock price prediction and trend forecasting

**Location:** `models/prediction.py` - `train_linear_regression()`

**Use Case:**
- Predicting future stock prices based on historical data
- Fast training and inference
- Works well for linear trends and short-term predictions

**Features Used:**
- Historical price data (Open, High, Low, Close)
- Trading volume
- Technical indicators (Moving Averages, Volatility)
- Temporal features (Day of week, Month)
- Daily returns

**Performance Metrics:**
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- R² Score (Coefficient of Determination)

---

### 1.2 Random Forest Regressor
**Purpose:** Advanced stock price prediction with non-linear relationships

**Location:** `models/prediction.py` - `train_random_forest()`

**Use Case:**
- Complex pattern recognition in stock price movements
- Handling non-linear relationships between features
- Better performance for long-term predictions
- Provides feature importance analysis

**Configuration:**
- n_estimators: 100 (number of decision trees)
- max_depth: 10 (maximum depth of each tree)
- n_jobs: -1 (parallel processing)

**Additional Outputs:**
- Feature importance scores
- Identifies which factors most influence price predictions

---

## 2. Natural Language Processing (NLP)

### 2.1 TextBlob Sentiment Analysis
**Purpose:** Analyzing sentiment from news articles and financial text

**Location:** `utils/sentiment.py` - `SentimentAnalyzer` class

**Use Case:**
- Evaluating market sentiment from news headlines
- Analyzing article descriptions and content
- Providing sentiment scores for investment decisions

**Metrics Provided:**
- **Polarity:** Ranges from -1 (negative) to +1 (positive)
- **Subjectivity:** Ranges from 0 (objective) to 1 (subjective)
- **Sentiment Category:** Positive, Negative, or Neutral
- **Confidence Score:** Absolute value of polarity

**Sentiment Classification:**
- Positive: polarity > 0.1
- Negative: polarity < -0.1
- Neutral: -0.1 ≤ polarity ≤ 0.1

---

## 3. Data Processing & Feature Engineering

### 3.1 MinMaxScaler
**Purpose:** Data normalization and preprocessing

**Location:** `models/prediction.py` - `StockPredictor` class

**Use Case:**
- Normalizing features to a common scale (0-1 range)
- Improving model convergence and performance
- Preventing features with larger values from dominating

---

### 3.2 Technical Indicators
**Purpose:** Feature extraction from price data

**Location:** 
- `utils/indicators.py` - Technical indicator calculations
- `models/prediction.py` - Feature preparation

**Indicators Used:**

#### Moving Averages (MA)
- **MA_5:** 5-day moving average
- **MA_10:** 10-day moving average  
- **MA_20:** 20-day moving average
- **Purpose:** Identify trends and smooth price volatility

#### Volatility
- **Calculation:** 10-day rolling standard deviation
- **Purpose:** Measure price fluctuation and risk

#### Daily Return
- **Calculation:** Percentage change in closing price
- **Purpose:** Measure daily performance

#### Additional Technical Indicators (from `utils/indicators.py`):
- **RSI (Relative Strength Index):** Momentum oscillator (0-100)
- **MACD (Moving Average Convergence Divergence):** Trend-following momentum
- **Bollinger Bands:** Volatility bands around moving average
- **OBV (On-Balance Volume):** Volume-based indicator
- **ATR (Average True Range):** Volatility measure
- **Stochastic Oscillator:** Momentum indicator

---

## 4. Model Evaluation & Validation

### 4.1 Train-Test Split
**Method:** Time-series aware split (no shuffling)

**Configuration:**
- Test size: 20% of data
- Shuffle: False (maintains temporal order)
- Random state: 42 (reproducibility)

**Purpose:**
- Evaluate model performance on unseen data
- Prevent overfitting
- Maintain chronological order for time-series data

---

### 4.2 Performance Metrics

#### RMSE (Root Mean Squared Error)
- Measures average prediction error
- Penalizes larger errors more heavily
- Same units as target variable (stock price)

#### MAE (Mean Absolute Error)
- Average absolute difference between predicted and actual values
- Less sensitive to outliers than RMSE

#### R² Score (Coefficient of Determination)
- Measures proportion of variance explained by the model
- Range: 0 (poor) to 1 (perfect fit)

---

## 5. Data Sources & APIs

### 5.1 yfinance
**Purpose:** Fetching real-time and historical stock data

**Location:** `utils/stock_data.py` - `StockDataFetcher` class

**Data Retrieved:**
- Historical OHLCV data (Open, High, Low, Close, Volume)
- Current stock prices
- Company information
- Financial metrics

---

### 5.2 NewsAPI
**Purpose:** Fetching financial news for sentiment analysis

**Location:** `utils/news.py` - `NewsAggregator` class

**Data Retrieved:**
- News headlines
- Article descriptions
- Publication dates
- Source information

---

## 6. Visualization & Analysis Tools

### 6.1 Plotly
**Purpose:** Interactive charts and visualizations

**Used For:**
- Price prediction charts
- Technical indicator overlays
- Performance comparison plots
- Interactive candlestick charts

### 6.2 Matplotlib
**Purpose:** Static charts and plots

**Used For:**
- Model performance visualization
- Feature importance plots
- Statistical analysis charts

---

## 7. Model Pipeline

### Prediction Pipeline Flow:
```
1. Data Collection (yfinance)
   ↓
2. Feature Engineering (Technical Indicators)
   ↓
3. Data Normalization (MinMaxScaler)
   ↓
4. Train-Test Split (Time-series aware)
   ↓
5. Model Training (Linear Regression / Random Forest)
   ↓
6. Prediction & Evaluation
   ↓
7. Future Price Forecasting
```

### Sentiment Analysis Pipeline:
```
1. News Collection (NewsAPI)
   ↓
2. Text Preprocessing
   ↓
3. Sentiment Analysis (TextBlob)
   ↓
4. Aggregation & Scoring
   ↓
5. Visualization & Insights
```

---

## 8. Model Selection Guidelines

### When to Use Linear Regression:
- ✅ Quick predictions needed
- ✅ Linear trends observed
- ✅ Short-term forecasting (days to weeks)
- ✅ Limited computational resources
- ✅ Interpretability is important

### When to Use Random Forest:
- ✅ Complex market patterns
- ✅ Non-linear relationships
- ✅ Long-term forecasting (weeks to months)
- ✅ Feature importance analysis needed
- ✅ Higher accuracy required

---

## 9. Python Version & Environment

**Python Version:** 3.13.9

**Key Libraries:**
- `streamlit` - Web application framework
- `scikit-learn` - Machine learning models
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `yfinance` - Stock data retrieval
- `textblob` - Sentiment analysis
- `plotly` - Interactive visualizations
- `matplotlib` - Static visualizations
- `ta` - Technical analysis indicators

---

## 10. Model Limitations & Considerations

### Important Notes:
1. **Past Performance ≠ Future Results:** Historical data may not predict future prices accurately
2. **Market Volatility:** Models may struggle during highly volatile periods
3. **External Factors:** Cannot account for breaking news, regulatory changes, or black swan events
4. **Data Quality:** Predictions are only as good as the input data
5. **Sentiment Limitations:** TextBlob provides basic sentiment; may miss context or sarcasm

### Best Practices:
- Use multiple models for comparison
- Combine technical analysis with fundamental analysis
- Consider sentiment analysis alongside predictions
- Regular model retraining with updated data
- Always validate predictions with domain knowledge

---

## Summary

This StockMarket application uses a combination of:
- **2 Supervised Learning Models** (Linear Regression, Random Forest)
- **1 NLP Technique** (TextBlob Sentiment Analysis)
- **10+ Technical Indicators** for feature engineering
- **1 Data Normalization Method** (MinMaxScaler)

All working together to provide comprehensive stock analysis and prediction capabilities.

---

*Last Updated: February 26, 2026*
*Python Version: 3.13.9*
