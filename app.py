"""
QuantEdge — Stock Market Intelligence Platform

A comprehensive Streamlit application for institutional-grade stock analysis:
  • Real-time market indices & stock data
  • AI-powered price predictions (Linear Regression, Random Forest)
  • 15+ technical indicators with multi-signal consensus
  • Fundamental analysis with financial health scoring
  • AI recommendation engine (weighted multi-factor)
  • Portfolio tracking with performance analytics
  • News aggregation with sentiment analysis
  • Premium dark-mode UI with professional finance design

Version: 4.0.0
"""

import streamlit as st
import config
from styles.theme import inject_css, page_header, market_ticker_bar, render_html

# Page configuration — MUST be first Streamlit command
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT,
    initial_sidebar_state="expanded",
)

# Inject premium CSS
inject_css()

# Import pages
from pages import (
    dashboard,
    stock_analysis,
    prediction,
    technical_indicators,
    portfolio_tracker,
    news_sentiment,
    ai_intelligence,
)


def _fetch_market_indices():
    """Fetch live market index data for the ticker bar."""
    indices_data = {}
    try:
        from utils.stock_data import StockDataFetcher
        for name, symbol in list(config.MARKET_INDICES.items())[:5]:
            try:
                fetcher = StockDataFetcher(symbol)
                price_info = fetcher.get_realtime_price()
                if price_info:
                    indices_data[name] = {
                        "price": price_info["current_price"],
                        "change": price_info["price_change"],
                        "pct": price_info["percent_change"],
                    }
            except Exception:
                pass
    except Exception:
        pass
    return indices_data


def main():
    """Main application entry point."""

    # ── Sidebar ──────────────────────────────────────────────
    with st.sidebar:
        # Brand header
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0 0.5rem 0;">
            <h1 style="
                color: #00D4FF;
                font-size: 1.7rem;
                font-weight: 900;
                margin: 0;
                letter-spacing: -0.03em;
            ">QuantEdge</h1>
            <p style="color: #546E7A; font-size: 0.72rem; margin: 0.2rem 0 0 0; letter-spacing: 0.08em; text-transform: uppercase; font-weight: 600;">
                Stock Intelligence
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color: rgba(0,212,255,0.08); margin: 0.8rem 0;'>",
                    unsafe_allow_html=True)

        # Navigation
        page = st.radio(
            "Navigation",
            config.SIDEBAR_OPTIONS,
            label_visibility="collapsed",
            key="nav_page",
        )

        st.markdown("<hr style='border-color: rgba(0,212,255,0.08); margin: 0.8rem 0;'>",
                    unsafe_allow_html=True)

        # Market status
        from datetime import datetime
        now = datetime.now()
        hour = now.hour
        is_market_hours = 9 <= hour < 16 and now.weekday() < 5
        status_color = "#00C853" if is_market_hours else "#FF9100"
        status_text = "MARKET OPEN" if is_market_hours else "MARKET CLOSED"

        st.markdown(f"""
        <div style="
            background: {status_color}10;
            border: 1px solid {status_color}30;
            border-radius: 8px;
            padding: 8px 12px;
            text-align: center;
            margin-bottom: 0.8rem;
        ">
            <span style="color: {status_color}; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.06em;">● {status_text}</span>
            <p style="color: #546E7A; font-size: 0.7rem; margin: 2px 0 0 0;">{now.strftime('%d %b %Y • %I:%M %p')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Quick info
        with st.expander("ℹ️ About", expanded=False):
            st.markdown(f"""
            <div style="font-size: 0.82rem; color: #78909C;">
                <p><strong style="color: #E8EAF6;">QuantEdge</strong> v{config.APP_VERSION}</p>
                <p>Stock market intelligence platform with AI-powered analytics.</p>
                <ul style="padding-left: 1rem; margin: 0.5rem 0;">
                    <li>Real-time market data</li>
                    <li>ML price predictions</li>
                    <li>15+ technical indicators</li>
                    <li>Fundamental scoring</li>
                    <li>AI recommendations</li>
                    <li>Portfolio analytics</li>
                    <li>News sentiment</li>
                </ul>
                <p style="color: #00D4FF; font-size: 0.75rem; margin-top: 0.5rem;">
                    ₹ INR  |  NSE / BSE / Global
                </p>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("🔗 Quick Links", expanded=False):
            st.markdown("""
            <div style="font-size: 0.82rem;">
                <a href="https://www.nseindia.com/" target="_blank" style="color: #00D4FF; text-decoration: none;">🇮🇳 NSE India</a><br>
                <a href="https://www.bseindia.com/" target="_blank" style="color: #00D4FF; text-decoration: none;">🇮🇳 BSE India</a><br>
                <a href="https://finance.yahoo.com/" target="_blank" style="color: #00D4FF; text-decoration: none;">📊 Yahoo Finance</a><br>
                <a href="https://www.moneycontrol.com/" target="_blank" style="color: #00D4FF; text-decoration: none;">📈 MoneyControl</a><br>
                <a href="https://www.bloomberg.com/" target="_blank" style="color: #00D4FF; text-decoration: none;">📰 Bloomberg</a>
            </div>
            """, unsafe_allow_html=True)

    # ── Market Indices Ticker Bar ─────────────────────────────
    page_idx = config.SIDEBAR_OPTIONS.index(page) if page in config.SIDEBAR_OPTIONS else 0

    if page_idx == 0:  # Dashboard
        indices = _fetch_market_indices()
        if indices:
            market_ticker_bar(indices)

    # ── Page Router ──────────────────────────────────────────
    page_map = {
        0: dashboard.show,
        1: stock_analysis.show,
        2: ai_intelligence.show,
        3: technical_indicators.show,
        4: prediction.show,
        5: portfolio_tracker.show,
        6: news_sentiment.show,
    }
    page_map.get(page_idx, dashboard.show)()


if __name__ == "__main__":
    main()
