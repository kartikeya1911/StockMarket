"""
Stock Market Analysis and Prediction Web Application

A comprehensive Streamlit-based application for stock market analysis, featuring:
- Real-time stock data and analysis
- Machine Learning price predictions (Linear Regression, Random Forest)
- Technical indicators (RSI, MACD, Bollinger Bands, Moving Averages)
- Portfolio tracking with automatic averaging
- News aggregation with sentiment analysis
- Interactive Plotly visualizations

Version: 2.0.0
Landing Page: Dashboard (Portfolio Overview)
"""

import streamlit as st
import config

# Import page modules
from pages import dashboard, stock_analysis, prediction, technical_indicators, portfolio_tracker, news_sentiment

# Page configuration
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    /* Main content area */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #312e81 100%);
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-size: 1rem;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    /* Headers */
    h1 {
        color: #1e40af;
        font-weight: 800;
    }
    
    h2 {
        color: #3730a3;
        font-weight: 700;
    }
    
    h3 {
        color: #4f46e5;
        font-weight: 600;
    }
    
    /* Cards effect */
    .stExpander {
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    
    .stSelectbox>div>div>select {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Sidebar navigation with enhanced UI
    st.sidebar.markdown("<h1 style='color: white; text-align: center;'>🎯 Navigation</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    
    # Page selection
    page = st.sidebar.radio(
        "Select a page:",
        config.SIDEBAR_OPTIONS,
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # About section with enhanced styling
    with st.sidebar.expander("ℹ️ About"):
        st.markdown(f"""
        <div style='color: white;'>
        <h3 style='color: #fbbf24;'>Stock Market Analyzer</h3>
        
        <p><strong>Version:</strong> {config.APP_VERSION}</p>
        
        <p style='font-size: 0.9rem;'>A comprehensive platform for stock market analysis,
        price prediction, and portfolio management.</p>
        
        <p style='font-size: 0.85rem; color: #d1d5db;'><strong>Features:</strong></p>
        <ul style='font-size: 0.85rem; color: #d1d5db;'>
            <li>Real-time stock data</li>
            <li>ML-based predictions</li>
            <li>Technical indicators</li>
            <li>Portfolio tracking</li>
            <li>News sentiment analysis</li>
        </ul>
        
        <p style='font-size: 0.8rem; color: #9ca3af; margin-top: 1rem;'>
        💰 Currency: Indian Rupee (₹)<br>
        📊 Markets: NSE, BSE
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick links with enhanced styling
    with st.sidebar.expander("🔗 Quick Links"):
        st.markdown("""
        <div style='color: white;'>
        <p style='font-size: 0.9rem;'>
        <a href='https://www.nseindia.com/' target='_blank' style='color: #60a5fa; text-decoration: none;'>🇮🇳 NSE India</a><br>
        <a href='https://www.bseindia.com/' target='_blank' style='color: #60a5fa; text-decoration: none;'>🇮🇳 BSE India</a><br>
        <a href='https://finance.yahoo.com/' target='_blank' style='color: #60a5fa; text-decoration: none;'>📊 Yahoo Finance</a><br>
        <a href='https://www.investing.com/' target='_blank' style='color: #60a5fa; text-decoration: none;'>💹 Investing.com</a><br>
        <a href='https://www.bloomberg.com/' target='_blank' style='color: #60a5fa; text-decoration: none;'>📰 Bloomberg</a>
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Route to appropriate page
    if page == "📊 My Dashboard":
        dashboard.show()
    elif page == "📈 Stock Analysis":
        stock_analysis.show()
    elif page == "🔮 Price Prediction":
        prediction.show()
    elif page == "📉 Technical Indicators":
        technical_indicators.show()
    elif page == "💼 Portfolio Tracker":
        portfolio_tracker.show()
    elif page == "📰 News & Sentiment":
        news_sentiment.show()

if __name__ == "__main__":
    main()
