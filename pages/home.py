"""
Home Page
Welcome page with overview and quick stats
"""

import streamlit as st
import config

def show():
    """Display home page"""
    
    # Hero section with gradient header
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 3rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                       font-weight: 800;'>📈 Stock Market Analysis & Prediction</h1>
            <p style='font-size: 1.3rem; color: #6b7280;'>Professional Stock Analysis Platform for Indian Markets</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Welcome to your comprehensive stock market analysis tool! This application provides
    real-time data, technical analysis, price predictions, and portfolio management.
    """)
    
    # Features overview
    st.markdown("---")
    st.header("🚀 Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 📊 Stock Analysis
        - Real-time stock data
        - Historical price charts
        - Interactive candlestick charts
        - Volume analysis
        - Company information
        """)
    
    with col2:
        st.markdown("""
        #### 🔮 Price Prediction
        - Machine Learning models
        - 30-day price forecasts
        - Model accuracy metrics
        - Linear & Random Forest
        - Feature importance
        """)
    
    with col3:
        st.markdown("""
        #### 📈 Technical Indicators
        - RSI (Relative Strength Index)
        - MACD Indicator
        - Bollinger Bands
        - Moving Averages
        - Trading signals
        """)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        #### 💼 Portfolio Tracker
        - Track multiple stocks
        - Calculate profit/loss
        - Portfolio allocation
        - Performance metrics
        - Best/worst performers
        """)
    
    with col5:
        st.markdown("""
        #### 📰 News & Sentiment
        - Latest stock news
        - Sentiment analysis
        - Market outlook
        - Investment signals
        - News aggregation
        """)
    
    with col6:
        st.markdown("""
        #### 📉 Market Insights
        - Support/Resistance levels
        - Volatility analysis
        - Trading volume trends
        - Price comparisons
        - Historical data
        """)
    
    # Quick start guide
    st.markdown("---")
    st.header("🎯 Quick Start Guide")
    
    st.markdown("""
    1. **Select a Feature** - Use the sidebar to navigate to different sections
    2. **Enter Stock Ticker** - Type a stock symbol (e.g., AAPL, TSLA, RELIANCE.NS)
    3. **Choose Time Period** - Select your preferred analysis timeframe
    4. **Analyze Results** - View charts, predictions, and recommendations
    5. **Manage Portfolio** - Add stocks to track your investments
    """)
    
    # Popular stock tickers
    st.markdown("---")
    st.header("🔥 Popular Stock Tickers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**US Stocks:**")
        st.code(", ".join(config.DEFAULT_STOCKS))
    
    with col2:
        st.markdown("**Indian Stocks:**")
        st.code(", ".join(config.INDIAN_STOCKS))
    
    # Tips section
    st.markdown("---")
    st.header("💡 Pro Tips")
    
    st.info("""
    - **For Indian stocks**, add `.NS` suffix (e.g., RELIANCE.NS)
    - **Use longer timeframes** for more accurate predictions
    - **Combine multiple indicators** for better trading decisions
    - **Check sentiment** before making investment decisions
    - **Diversify your portfolio** to minimize risk
    """)
    
    # Disclaimer
    st.markdown("---")
    st.warning("""
    **⚠️ Disclaimer:** This application is for educational and informational purposes only.
    It should not be considered as financial advice. Always do your own research and consult
    with a qualified financial advisor before making investment decisions.
    """)
    
    # Footer with enhanced design
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; padding: 2rem 0;'>
            <p style='color: #6b7280; font-size: 0.9rem;'>
                Made with ❤️ using Streamlit | Version 1.0.0<br>
                <span style='font-size: 0.85rem;'>Supports Indian Stock Market (NSE/BSE) with ₹ INR Currency</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
