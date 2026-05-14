"""
Stock Analysis Page — Comprehensive stock analysis with charts, fundamentals, and volume.
"""

import streamlit as st
import pandas as pd
from utils.stock_data import StockDataFetcher, format_large_number, format_currency
from utils.charts import create_line_chart, create_candlestick_chart, create_volume_chart, create_ma_chart
from styles.theme import page_header, gradient_card, glass_card, metric_row, render_html
import config


def show():
    """Display the stock analysis page."""

    page_header("Stock Analysis", "Real-time data, charts, and fundamental insights", "🔍")

    # ── Inputs ───────────────────────────────────────────────
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        ticker = st.text_input("Enter Stock Ticker", value="AAPL",
                               help="e.g., AAPL, TSLA, GOOGL, RELIANCE.NS").upper()
    with col2:
        period = st.selectbox("Time Period", list(config.TIME_PERIODS.keys()), index=3)
    with col3:
        interval = st.selectbox("Interval", list(config.DATA_INTERVALS.keys()), index=0)

    analyze = st.button("🔍 Analyze Stock", type="primary", use_container_width=True)

    if analyze or 'sa_ticker' in st.session_state:
        if analyze:
            st.session_state.sa_ticker = ticker
            st.session_state.sa_period = period
            st.session_state.sa_interval = interval

        ticker = st.session_state.sa_ticker
        period = st.session_state.sa_period
        interval = st.session_state.sa_interval

        with st.spinner(config.LOADING_MESSAGES['fetching_data']):
            fetcher = StockDataFetcher(ticker)
            if not fetcher.validate_ticker():
                st.error(config.ERROR_MESSAGES['invalid_ticker'])
                return

            stock_info = fetcher.get_stock_info()
            if not stock_info:
                st.error(config.ERROR_MESSAGES['no_data'])
                return

            hist_data = fetcher.get_historical_data(
                period=config.TIME_PERIODS[period],
                interval=config.DATA_INTERVALS[interval]
            )
            if hist_data is None or hist_data.empty:
                st.error(config.ERROR_MESSAGES['no_data'])
                return

        # ── Header Metrics ───────────────────────────────────
        st.markdown("---")

        current_price = stock_info['current_price']
        prev_close = stock_info['previous_close']
        price_change = current_price - prev_close
        pct_change = (price_change / prev_close * 100) if prev_close else 0

        # Title
        render_html(f"""
        <div style="margin-bottom: 1rem;">
            <h2 style="color: #E8EAF6; margin: 0;">{stock_info['name']}</h2>
            <p style="color: #78909C; margin: 0;">{stock_info['symbol']} · {stock_info.get('sector', 'N/A')} · {stock_info.get('industry', 'N/A')}</p>
        </div>
        """)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Current Price", format_currency(current_price),
                      f"{price_change:+.2f} ({pct_change:+.2f}%)")
        with col2:
            st.metric("Market Cap", format_large_number(stock_info['market_cap']))
        with col3:
            st.metric("Day High", format_currency(stock_info['day_high']))
        with col4:
            st.metric("Day Low", format_currency(stock_info['day_low']))
        with col5:
            st.metric("Volume", format_large_number(stock_info['volume']))

        # ── Fundamentals ─────────────────────────────────────
        with st.expander("📋 Fundamental Data & Growth Metrics", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                pe = stock_info.get('pe_ratio', 0)
                render_html(metric_row("PE Ratio", f"{pe:.2f}" if pe else "N/A"))
                roe = stock_info.get('roe', 0)
                render_html(metric_row("ROE", f"{roe*100:.2f}%" if roe else "N/A", "#00D4FF" if roe and roe > 0 else "#FF5252"))
                beta = stock_info.get('beta', 0)
                render_html(metric_row("Beta", f"{beta:.2f}" if beta else "N/A"))
            with c2:
                rev_g = stock_info.get('revenue_growth', 0)
                render_html(metric_row("Sales Growth (YoY)", f"{rev_g*100:+.2f}%" if rev_g else "N/A", "#00C853" if rev_g and rev_g > 0 else "#FF5252"))
                q_g = stock_info.get('quarterly_growth', 0)
                render_html(metric_row("Quarterly Growth", f"{q_g*100:+.2f}%" if q_g else "N/A", "#00C853" if q_g and q_g > 0 else "#FF5252"))
                div_y = stock_info.get('dividend_yield', 0)
                render_html(metric_row("Div Yield", f"{div_y*100:.2f}%" if div_y else "N/A"))
            with c3:
                cagr_3y = stock_info.get('cagr_3y', 0)
                render_html(metric_row("3Y CAGR", f"{cagr_3y*100:+.2f}%" if cagr_3y else "N/A", "#00C853" if cagr_3y and cagr_3y > 0 else "#FF5252"))
                cagr_5y = stock_info.get('cagr_5y', 0)
                render_html(metric_row("5Y CAGR", f"{cagr_5y*100:+.2f}%" if cagr_5y else "N/A", "#00C853" if cagr_5y and cagr_5y > 0 else "#FF5252"))
                render_html(metric_row("Sector", stock_info.get('sector', 'N/A')))
            with c4:
                render_html(metric_row("52W High", format_currency(stock_info.get('52_week_high', 0))))
                render_html(metric_row("52W Low", format_currency(stock_info.get('52_week_low', 0))))
                render_html(metric_row("Industry", stock_info.get('industry', 'N/A')))

        # ── Charts ───────────────────────────────────────────
        st.markdown("---")
        st.subheader("📈 Price Charts")

        chart_type = st.radio("Chart Type", ["Line Chart", "Candlestick"], horizontal=True)

        if chart_type == "Line Chart":
            fig = create_line_chart(hist_data, title=f"{ticker} — {period}")
        else:
            fig = create_candlestick_chart(hist_data, title=f"{ticker} — {period}")
        st.plotly_chart(fig, use_container_width=True)

        # Volume
        st.subheader("📊 Volume")
        vol_fig = create_volume_chart(hist_data)
        st.plotly_chart(vol_fig, use_container_width=True)

        # ── Historical Data ──────────────────────────────────
        st.markdown("---")
        st.subheader("📑 Historical Data")

        display_data = hist_data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
        display_data['Date'] = pd.to_datetime(display_data['Date']).dt.strftime('%Y-%m-%d')

        st.dataframe(
            display_data.tail(20).sort_values('Date', ascending=False),
            use_container_width=True,
            hide_index=True
        )

        csv = display_data.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{ticker}_data.csv",
            mime="text/csv"
        )

