"""
Stock Analysis Page
Displays comprehensive stock analysis with charts and metrics
"""

import streamlit as st
import pandas as pd
from utils.stock_data import StockDataFetcher, format_large_number, format_currency
from utils.charts import (
    create_line_chart, create_candlestick_chart, 
    create_volume_chart, create_ma_chart
)
import config

def show():
    """Display stock analysis page"""
    
    st.markdown("""
        <h1 style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📊 Stock Analysis Dashboard</h1>
        <p style='font-size: 1.1rem; color: #6b7280;'>Analyze stocks with real-time data and interactive charts</p>
    """, unsafe_allow_html=True)
    
    # Input section
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        ticker = st.text_input(
            "Enter Stock Ticker",
            value="AAPL",
            help="e.g., AAPL, TSLA, GOOGL, RELIANCE.NS"
        ).upper()
    
    with col2:
        period = st.selectbox(
            "Time Period",
            options=list(config.TIME_PERIODS.keys()),
            index=3
        )
    
    with col3:
        interval = st.selectbox(
            "Interval",
            options=list(config.DATA_INTERVALS.keys()),
            index=0
        )
    
    analyze_button = st.button("🔍 Analyze Stock", type="primary")
    
    if analyze_button or 'current_ticker' in st.session_state:
        if analyze_button:
            st.session_state.current_ticker = ticker
            st.session_state.current_period = period
            st.session_state.current_interval = interval
        
        ticker = st.session_state.current_ticker
        period = st.session_state.current_period
        interval = st.session_state.current_interval
        
        # Fetch data
        with st.spinner(config.LOADING_MESSAGES['fetching_data']):
            fetcher = StockDataFetcher(ticker)
            
            if not fetcher.validate_ticker():
                st.error(config.ERROR_MESSAGES['invalid_ticker'])
                return
            
            # Get stock info
            stock_info = fetcher.get_stock_info()
            if not stock_info:
                st.error(config.ERROR_MESSAGES['no_data'])
                return
            
            # Get historical data
            hist_data = fetcher.get_historical_data(
                period=config.TIME_PERIODS[period],
                interval=config.DATA_INTERVALS[interval]
            )
            
            if hist_data is None or hist_data.empty:
                st.error(config.ERROR_MESSAGES['no_data'])
                return
        
        st.success(config.SUCCESS_MESSAGES['data_loaded'])
        
        # Display stock information
        st.markdown("---")
        st.header(f"{stock_info['name']} ({stock_info['symbol']})")
        
        # Key metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        current_price = stock_info['current_price']
        previous_close = stock_info['previous_close']
        price_change = current_price - previous_close
        percent_change = (price_change / previous_close * 100) if previous_close else 0
        
        with col1:
            st.metric(
                "Current Price",
                format_currency(current_price),
                f"{price_change:+.2f} ({percent_change:+.2f}%)"
            )
        
        with col2:
            st.metric("Market Cap", format_large_number(stock_info['market_cap']))
        
        with col3:
            st.metric("Day High", format_currency(stock_info['day_high']))
        
        with col4:
            st.metric("Day Low", format_currency(stock_info['day_low']))
        
        with col5:
            st.metric("Volume", format_large_number(stock_info['volume']))
        
        # Additional info
        with st.expander("📋 Additional Information"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**52 Week High:** {format_currency(stock_info['52_week_high'])}")
                st.write(f"**52 Week Low:** {format_currency(stock_info['52_week_low'])}")
                st.write(f"**PE Ratio:** {stock_info['pe_ratio']:.2f}" if stock_info['pe_ratio'] else "**PE Ratio:** N/A")
            
            with col2:
                st.write(f"**Beta:** {stock_info['beta']:.2f}" if stock_info['beta'] else "**Beta:** N/A")
                st.write(f"**Sector:** {stock_info['sector']}")
                st.write(f"**Industry:** {stock_info['industry']}")
            
            with col3:
                dividend = stock_info['dividend_yield']
                if dividend:
                    st.write(f"**Dividend Yield:** {dividend*100:.2f}%")
                else:
                    st.write(f"**Dividend Yield:** N/A")
        
        # Charts section
        st.markdown("---")
        st.header("📈 Price Charts")
        
        chart_type = st.radio(
            "Select Chart Type",
            ["Line Chart", "Candlestick Chart"],
            horizontal=True
        )
        
        if chart_type == "Line Chart":
            fig = create_line_chart(
                hist_data,
                title=f"{ticker} Stock Price - {period}"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = create_candlestick_chart(
                hist_data,
                title=f"{ticker} Candlestick Chart - {period}"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Volume chart
        st.subheader("📊 Trading Volume")
        vol_fig = create_volume_chart(hist_data)
        st.plotly_chart(vol_fig, use_container_width=True)
        
        # Historical data table
        st.markdown("---")
        st.header("📑 Historical Data")
        
        display_data = hist_data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
        display_data['Date'] = pd.to_datetime(display_data['Date']).dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            display_data.tail(20).sort_values('Date', ascending=False),
            use_container_width=True,
            hide_index=True
        )
        
        # Download button
        csv = display_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"{ticker}_historical_data.csv",
            mime="text/csv"
        )
