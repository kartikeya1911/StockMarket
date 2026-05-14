"""
Dashboard Page — QuantEdge portfolio overview with market data.
"""

import streamlit as st
import pandas as pd
from utils.stock_data import format_currency, format_large_number
from utils.portfolio import PortfolioManager
from utils.charts import create_portfolio_allocation_chart
from utils.news import NewsFetcher
from styles.theme import (
    page_header, gradient_card, stat_card, glass_card,
    section_header, metric_row, render_html,
)
from datetime import datetime


def show():
    """Display the portfolio dashboard."""

    page_header("Dashboard", "Portfolio overview & market intelligence", "📊")

    # Initialize
    portfolio_mgr = PortfolioManager()
    summary = portfolio_mgr.get_portfolio_summary()

    if summary is None or summary['total_stocks'] == 0:
        _show_empty_state()
        return

    # ── KPI Cards ────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_html(
            stat_card("Total Investment", format_currency(summary['total_investment']),
                      sublabel="Cost basis")
        )
    with col2:
        render_html(
            stat_card("Current Value", format_currency(summary['current_value']),
                      sublabel="Market value")
        )
    with col3:
        gl = summary['total_gain_loss']
        gl_pct = summary['total_gain_loss_percent']
        color = "#00C853" if gl >= 0 else "#FF5252"
        arrow = "▲" if gl >= 0 else "▼"
        render_html(
            stat_card("Total P&L", format_currency(gl),
                      change=f"{arrow} {abs(gl_pct):.2f}%", change_color=color,
                      sublabel="Unrealized")
        )
    with col4:
        render_html(
            stat_card("Holdings", str(summary['total_stocks']),
                      sublabel="Active positions")
        )

    st.write("")

    # ── Holdings & Allocation ────────────────────────────────
    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        section_header("📋 Holdings", "Real-time positions")
        if summary['portfolio_details'] is not None:
            details = summary['portfolio_details'].copy()

            display_df = details[['Ticker', 'Company_Name', 'Quantity', 'Purchase_Price',
                                  'Current_Price', 'Investment', 'Current_Value',
                                  'Gain_Loss', 'Gain_Loss_Percent']].copy()
            display_df.columns = ['Ticker', 'Company', 'Qty', 'Buy Price', 'Current',
                                  'Invested', 'Value', 'P&L', 'P&L %']

            st.dataframe(
                display_df.style.format({
                    'Qty': '{:.2f}',
                    'Buy Price': '₹{:,.2f}',
                    'Current': '₹{:,.2f}',
                    'Invested': '₹{:,.2f}',
                    'Value': '₹{:,.2f}',
                    'P&L': '₹{:,.2f}',
                    'P&L %': '{:+.2f}%',
                }).map(
                    lambda v: f'color: {"#00C853" if v >= 0 else "#FF5252"}' if isinstance(v, (int, float)) else '',
                    subset=['P&L', 'P&L %']
                ),
                use_container_width=True,
                hide_index=True,
                height=min(400, len(display_df) * 50 + 60),
            )

    with col_right:
        section_header("📊 Allocation", "By current value")
        allocation = portfolio_mgr.get_portfolio_allocation()
        if allocation is not None:
            fig = create_portfolio_allocation_chart(allocation)
            st.plotly_chart(fig, use_container_width=True)

    # ── Best & Worst Performers ──────────────────────────────
    st.markdown("---")
    col1, col2 = st.columns(2)

    performers = portfolio_mgr.get_best_worst_performers()
    if performers:
        with col1:
            best = performers['best']
            content = f"""
                <p style="color: #78909C; font-size: 0.78rem; margin: 0; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase;">🏆 Top Performer</p>
                <h3 style="color: #00C853; margin: 0.3rem 0; font-size: 1.1rem;">{best['ticker']}</h3>
                <p style="color: #E8EAF6; font-size: 0.85rem; margin: 0;">{best['company']}</p>
                <p style="color: #00C853; font-size: 1.05rem; font-weight: 700; margin: 0.3rem 0; font-family: 'JetBrains Mono', monospace;">
                    {format_currency(best['gain_loss'])} ({best['gain_loss_percent']:+.2f}%)
                </p>
            """
            render_html(glass_card(content))

        with col2:
            worst = performers['worst']
            content = f"""
                <p style="color: #78909C; font-size: 0.78rem; margin: 0; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase;">📉 Worst Performer</p>
                <h3 style="color: #FF5252; margin: 0.3rem 0; font-size: 1.1rem;">{worst['ticker']}</h3>
                <p style="color: #E8EAF6; font-size: 0.85rem; margin: 0;">{worst['company']}</p>
                <p style="color: #FF5252; font-size: 1.05rem; font-weight: 700; margin: 0.3rem 0; font-family: 'JetBrains Mono', monospace;">
                    {format_currency(worst['gain_loss'])} ({worst['gain_loss_percent']:+.2f}%)
                </p>
            """
            render_html(glass_card(content))

    # ── Latest News ──────────────────────────────────────────
    if summary['portfolio_details'] is not None:
        st.markdown("---")
        section_header("📰 Portfolio News Feed", "Latest headlines for your holdings")

        news_fetcher = NewsFetcher()
        stock_list = summary['portfolio_details']['Ticker'].tolist()

        for ticker in stock_list[:5]:
            with st.expander(f"📊 {ticker}", expanded=False):
                try:
                    articles = news_fetcher.fetch_stock_news(ticker, days_back=7, max_articles=1)
                    if articles and len(articles) > 0:
                        article = articles[0]
                        title = article.get('title', 'No title')
                        url = article.get('url', '#')
                        source = article.get('source', {}).get('name', 'Unknown')
                        desc = article.get('description', '')

                        st.markdown(f"**[{title}]({url})**")
                        st.caption(f"Source: {source}")
                        if desc:
                            st.write(desc[:200] + "..." if len(desc) > 200 else desc)
                    else:
                        st.info(f"No recent news for {ticker}")
                except Exception:
                    st.info(f"Unable to load news for {ticker}")


def _show_empty_state():
    """Show empty portfolio state."""
    render_html("""
    <div style="
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(15, 20, 50, 0.85);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        margin: 2rem 0;
    ">
        <h2 style="color: #00D4FF; margin-bottom: 0.5rem;">Welcome to QuantEdge</h2>
        <p style="color: #78909C; font-size: 1.05rem; margin-bottom: 1.5rem;">
            Your portfolio is empty. Start by adding stocks to track your investments.
        </p>
        <p style="color: #E8EAF6; font-size: 0.92rem;">
            Navigate to <strong>💼 Portfolio Tracker</strong> to add your first stock.
        </p>
    </div>
    """)

    st.write("")

    section_header("🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        content = """
            <p style="color: #00D4FF; font-weight: 600; margin: 0;">🔍 Analyze Stocks</p>
            <p style="color: #78909C; font-size: 0.82rem; margin: 0.3rem 0 0 0;">
                Technical &amp; fundamental analysis
            </p>
        """
        render_html(glass_card(content))
    with col2:
        content = """
            <p style="color: #00C853; font-weight: 600; margin: 0;">🤖 AI Intelligence</p>
            <p style="color: #78909C; font-size: 0.82rem; margin: 0.3rem 0 0 0;">
                Weighted AI recommendations
            </p>
        """
        render_html(glass_card(content))
    with col3:
        content = """
            <p style="color: #FFD740; font-weight: 600; margin: 0;">🔮 Price Prediction</p>
            <p style="color: #78909C; font-size: 0.82rem; margin: 0.3rem 0 0 0;">
                ML-powered forecasting
            </p>
        """
        render_html(glass_card(content))

