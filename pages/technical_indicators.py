"""
Technical Indicators Page
Display and analyze technical indicators
"""

import streamlit as st
from utils.stock_data import StockDataFetcher
from utils.indicators import TechnicalIndicators
from utils.charts import create_ma_chart, create_rsi_chart, create_macd_chart, create_bollinger_bands_chart
import config

def show():
    """Display technical indicators page"""
    
    st.markdown("""
        <h1 style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📈 Technical Indicators</h1>
        <p style='font-size: 1.1rem; color: #6b7280;'>Advanced technical analysis with trading signals</p>
    """, unsafe_allow_html=True)
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        ticker = st.text_input(
            "Enter Stock Ticker",
            value="AAPL",
            help="e.g., AAPL, TSLA, GOOGL"
        ).upper()
    
    with col2:
        period = st.selectbox(
            "Time Period",
            ["6 Months", "1 Year", "2 Years"],
            index=1
        )
    
    analyze_button = st.button("📊 Analyze Indicators", type="primary")
    
    if analyze_button or 'indicator_data' in st.session_state:
        if analyze_button:
            # Fetch data
            with st.spinner(config.LOADING_MESSAGES['calculating']):
                fetcher = StockDataFetcher(ticker)
                
                if not fetcher.validate_ticker():
                    st.error(config.ERROR_MESSAGES['invalid_ticker'])
                    return
                
                period_map = {"6 Months": "6mo", "1 Year": "1y", "2 Years": "2y"}
                hist_data = fetcher.get_historical_data(period=period_map[period])
                
                if hist_data is None or hist_data.empty:
                    st.error(config.ERROR_MESSAGES['no_data'])
                    return
                
                stock_info = fetcher.get_stock_info()
                current_price = stock_info['current_price'] if stock_info else hist_data['Close'].iloc[-1]
                
                # Calculate indicators
                tech_indicators = TechnicalIndicators(hist_data)
                data_with_indicators = tech_indicators.calculate_all_indicators()
            
            # Store in session state
            st.session_state.indicator_data = {
                'ticker': ticker,
                'data': data_with_indicators,
                'current_price': current_price,
                'tech_indicators': tech_indicators
            }
        
        # Retrieve from session state
        stored_data = st.session_state.indicator_data
        ticker = stored_data['ticker']
        data = stored_data['data']
        current_price = stored_data['current_price']
        tech_indicators = stored_data['tech_indicators']
        
        st.success("✅ Indicators calculated successfully!")
        
        # Moving Averages
        st.markdown("---")
        st.header("📊 Moving Averages")
        
        if 'SMA_50' in data.columns and 'SMA_200' in data.columns:
            ma_signal = tech_indicators.get_moving_average_signal(
                data['SMA_50'],
                data['SMA_200']
            )
            
            col1, col2 = st.columns([2, 1])
            
            with col2:
                st.markdown(f"### Signal: {ma_signal['signal']}")
                st.markdown(f"**{ma_signal['message']}**")
            
            with col1:
                fig = create_ma_chart(data, ['SMA_50', 'SMA_200'])
                st.plotly_chart(fig, use_container_width=True)
        
        # RSI
        st.markdown("---")
        st.header("📉 RSI (Relative Strength Index)")
        
        if 'RSI' in data.columns:
            current_rsi = data['RSI'].iloc[-1]
            rsi_signal = tech_indicators.get_rsi_signal(current_rsi)
            
            col1, col2 = st.columns([2, 1])
            
            with col2:
                st.metric("Current RSI", f"{current_rsi:.2f}")
                st.markdown(f"### {rsi_signal['signal']}")
                st.markdown(f"**{rsi_signal['message']}**")
                
                # RSI interpretation
                st.markdown("**RSI Levels:**")
                st.markdown("- Above 70: Overbought")
                st.markdown("- Below 30: Oversold")
                st.markdown("- 30-70: Neutral")
            
            with col1:
                fig = create_rsi_chart(data)
                st.plotly_chart(fig, use_container_width=True)
        
        # MACD
        st.markdown("---")
        st.header("📊 MACD (Moving Average Convergence Divergence)")
        
        if 'MACD' in data.columns:
            macd_data = {
                'macd': data['MACD'],
                'signal': data['MACD_Signal'],
                'histogram': data['MACD_Histogram']
            }
            macd_signal = tech_indicators.get_macd_signal(macd_data)
            
            col1, col2 = st.columns([2, 1])
            
            with col2:
                st.markdown(f"### {macd_signal['signal']}")
                st.markdown(f"**{macd_signal['message']}**")
                
                # MACD values
                st.metric("MACD", f"{data['MACD'].iloc[-1]:.2f}")
                st.metric("Signal", f"{data['MACD_Signal'].iloc[-1]:.2f}")
                st.metric("Histogram", f"{data['MACD_Histogram'].iloc[-1]:.2f}")
            
            with col1:
                fig = create_macd_chart(data)
                st.plotly_chart(fig, use_container_width=True)
        
        # Bollinger Bands
        st.markdown("---")
        st.header("📈 Bollinger Bands")
        
        if 'BB_Upper' in data.columns:
            bb_data = {
                'upper': data['BB_Upper'],
                'middle': data['BB_Middle'],
                'lower': data['BB_Lower']
            }
            bb_signal = tech_indicators.get_bollinger_signal(bb_data, current_price)
            
            col1, col2 = st.columns([2, 1])
            
            with col2:
                st.markdown(f"### {bb_signal['signal']}")
                st.markdown(f"**{bb_signal['message']}**")
                
                # Band values
                st.metric("Upper Band", f"₹{data['BB_Upper'].iloc[-1]:.2f}")
                st.metric("Middle Band", f"₹{data['BB_Middle'].iloc[-1]:.2f}")
                st.metric("Lower Band", f"₹{data['BB_Lower'].iloc[-1]:.2f}")
            
            with col1:
                fig = create_bollinger_bands_chart(data)
                st.plotly_chart(fig, use_container_width=True)
        
        # Summary
        st.markdown("---")
        st.header("📋 Trading Signals Summary")
        
        signals_df = {
            "Indicator": ["Moving Averages", "RSI", "MACD", "Bollinger Bands"],
            "Signal": [
                ma_signal['signal'],
                rsi_signal['signal'],
                macd_signal['signal'],
                bb_signal['signal']
            ],
            "Recommendation": [
                ma_signal['message'],
                rsi_signal['message'],
                macd_signal['message'],
                bb_signal['message']
            ]
        }
        
        import pandas as pd
        st.dataframe(pd.DataFrame(signals_df), use_container_width=True, hide_index=True)
        
        # Disclaimer
        st.info("""
        **⚠️ Important:** Technical indicators are tools for analysis and should not be used
        in isolation. Always consider multiple factors and consult with financial professionals
        before making investment decisions.
        """)
