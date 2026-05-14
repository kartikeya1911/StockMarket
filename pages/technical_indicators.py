"""
Technical Indicators Page — All indicators with trading signal summary.
"""

import streamlit as st
import pandas as pd
from utils.stock_data import StockDataFetcher
from utils.indicators import TechnicalIndicators
from utils.charts import create_ma_chart, create_rsi_chart, create_macd_chart, create_bollinger_bands_chart
from styles.theme import page_header, glass_card, signal_badge, metric_row, render_html
import config


def show():
    """Display the technical indicators page."""

    page_header("Technical Indicators", "Advanced technical analysis with trading signals", "📉")

    # ── Inputs ───────────────────────────────────────────────
    col1, col2 = st.columns([2, 1])
    with col1:
        ticker = st.text_input("Enter Stock Ticker", value="AAPL",
                               help="e.g., AAPL, TSLA, GOOGL").upper()
    with col2:
        period = st.selectbox("Time Period", ["6 Months", "1 Year", "2 Years"], index=1)

    analyze = st.button("📊 Analyze Indicators", type="primary", use_container_width=True)

    if analyze or 'ti_data' in st.session_state:
        if analyze:
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

                tech = TechnicalIndicators(hist_data)
                data = tech.calculate_all_indicators()

            st.session_state.ti_data = {
                'ticker': ticker,
                'data': data,
                'current_price': current_price,
                'tech': tech,
            }

        stored = st.session_state.ti_data
        ticker = stored['ticker']
        data = stored['data']
        current_price = stored['current_price']
        tech = stored['tech']

        # Collect signals for summary
        all_signals = {}

        # ── Moving Averages ──────────────────────────────────
        st.markdown("---")
        st.subheader("📊 Moving Averages")

        if 'SMA_50' in data.columns and 'SMA_200' in data.columns:
            ma_signal = tech.get_moving_average_signal(data['SMA_50'], data['SMA_200'])
            all_signals['Moving Averages'] = ma_signal

            col1, col2 = st.columns([2.5, 1])
            with col1:
                fig = create_ma_chart(data, ['SMA_50', 'SMA_200'])
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                _render_signal_card("Moving Average Cross", ma_signal)

        # ── RSI ──────────────────────────────────────────────
        st.markdown("---")
        st.subheader("📉 RSI (Relative Strength Index)")

        if 'RSI' in data.columns:
            rsi_val = data['RSI'].iloc[-1]
            rsi_signal = tech.get_rsi_signal(rsi_val)
            all_signals['RSI'] = rsi_signal

            col1, col2 = st.columns([2.5, 1])
            with col1:
                fig = create_rsi_chart(data)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                _render_signal_card("RSI", rsi_signal, extra=f"Value: {rsi_val:.2f}")

        # ── MACD ─────────────────────────────────────────────
        st.markdown("---")
        st.subheader("📊 MACD")

        if 'MACD' in data.columns:
            macd_data = {
                'macd': data['MACD'],
                'signal': data['MACD_Signal'],
                'histogram': data['MACD_Histogram'],
            }
            macd_signal = tech.get_macd_signal(macd_data)
            all_signals['MACD'] = macd_signal

            col1, col2 = st.columns([2.5, 1])
            with col1:
                fig = create_macd_chart(data)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                _render_signal_card("MACD", macd_signal,
                                    extra=f"MACD: {data['MACD'].iloc[-1]:.4f}")

        # ── Bollinger Bands ──────────────────────────────────
        st.markdown("---")
        st.subheader("📈 Bollinger Bands")

        if 'BB_Upper' in data.columns:
            bb_data = {
                'upper': data['BB_Upper'],
                'middle': data['BB_Middle'],
                'lower': data['BB_Lower'],
            }
            bb_signal = tech.get_bollinger_signal(bb_data, current_price)
            all_signals['Bollinger Bands'] = bb_signal

            col1, col2 = st.columns([2.5, 1])
            with col1:
                fig = create_bollinger_bands_chart(data)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                _render_signal_card("Bollinger Bands", bb_signal,
                                    extra=f"Upper: ₹{data['BB_Upper'].iloc[-1]:.2f} | Lower: ₹{data['BB_Lower'].iloc[-1]:.2f}")

        # ── Signals Summary ──────────────────────────────────
        if all_signals:
            st.markdown("---")
            st.subheader("📋 Trading Signals Summary")

            sig_rows = []
            for name, sig in all_signals.items():
                sig_rows.append({
                    "Indicator": name,
                    "Signal": sig.get('signal', 'N/A'),
                    "Analysis": sig.get('message', 'N/A'),
                })

            df = pd.DataFrame(sig_rows)
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Consensus
            bullish = sum(1 for s in all_signals.values()
                          if any(w in s.get('signal', '').lower() for w in ['bullish', 'golden', 'oversold']))
            bearish = sum(1 for s in all_signals.values()
                          if any(w in s.get('signal', '').lower() for w in ['bearish', 'death', 'overbought']))
            total = len(all_signals)

            if bullish > bearish:
                consensus = "Bullish"
                color = "#00C853"
            elif bearish > bullish:
                consensus = "Bearish"
                color = "#FF5252"
            else:
                consensus = "Neutral"
                color = "#FFD740"

            render_html(f"""
            <div style="
                background: {color}15;
                border: 1px solid {color}44;
                border-radius: 12px;
                padding: 1rem 1.5rem;
                text-align: center;
                margin: 1rem 0;
            ">
                <p style="color: #78909C; margin: 0; font-size: 0.85rem;">Multi-Indicator Consensus</p>
                <h3 style="color: {color}; margin: 0.3rem 0;">{consensus}</h3>
                <p style="color: #78909C; margin: 0; font-size: 0.85rem;">
                    {bullish} Bullish · {bearish} Bearish · {total - bullish - bearish} Neutral
                </p>
            </div>
            """)

        st.markdown("---")
        st.info("""
        **⚠️ Important:** Technical indicators should not be used in isolation.
        Use the **🤖 AI Intelligence** page for comprehensive multi-factor analysis.
        """)


def _render_signal_card(title: str, signal: dict, extra: str = ""):
    """Render a signal card in the sidebar-like right column."""
    sig_text = signal.get('signal', 'N/A')
    msg = signal.get('message', '')
    color_map = {
        'green': '#00C853', 'red': '#FF5252', 'orange': '#FFD740',
        'lightgreen': '#00C853', 'gray': '#78909C',
    }
    color = color_map.get(signal.get('color', 'gray'), '#78909C')

    content = f"""
        <p style="color: #78909C; font-size: 0.8rem; margin: 0;">{title}</p>
        <p style="color: {color}; font-size: 1.1rem; font-weight: 700; margin: 0.3rem 0;">{sig_text}</p>
        <p style="color: #E8EAF6; font-size: 0.85rem; margin: 0;">{msg}</p>
    """
    if extra:
        content += f'<p style="color: #78909C; font-size: 0.8rem; margin: 0.3rem 0 0 0;">{extra}</p>'

    render_html(glass_card(content))

