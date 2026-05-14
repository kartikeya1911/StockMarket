"""
Portfolio Tracker Page — Add/remove stocks and monitor performance.
"""

import streamlit as st
import pandas as pd
from utils.portfolio import PortfolioManager, calculate_portfolio_metrics
from utils.charts import create_portfolio_allocation_chart
from utils.stock_data import format_currency
from styles.theme import page_header, gradient_card, glass_card, metric_row, render_html
from datetime import datetime


def show():
    """Display the portfolio tracker page."""

    page_header("Portfolio Tracker", "Track your investments and monitor performance", "💼")

    portfolio_mgr = PortfolioManager()

    # ── Add Stock Form ───────────────────────────────────────
    st.subheader("➕ Add Stock")

    with st.form("add_stock_form"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            new_ticker = st.text_input("Ticker Symbol",
                                       help="e.g., AAPL, TSLA, RELIANCE.NS").upper()
        with col2:
            quantity = st.number_input("Quantity", min_value=0.01, value=1.0, step=0.01)
        with col3:
            purchase_price = st.number_input("Purchase Price (₹)", min_value=0.01, value=100.0, step=0.01)
        with col4:
            purchase_date = st.date_input("Purchase Date")

        submitted = st.form_submit_button("Add to Portfolio", type="primary", use_container_width=True)

        if submitted:
            if new_ticker:
                success = portfolio_mgr.add_stock(
                    new_ticker, quantity, purchase_price,
                    purchase_date.strftime('%Y-%m-%d')
                )
                if success:
                    st.success(f"✅ Added {new_ticker} to portfolio!")
                    st.rerun()
                else:
                    st.error("Failed to add stock. Please check the ticker symbol.")
            else:
                st.error("Please enter a ticker symbol")

    # ── Portfolio Summary ────────────────────────────────────
    summary = portfolio_mgr.get_portfolio_summary()

    if summary is None or summary['total_stocks'] == 0:
        render_html("""
        <div style="
            text-align: center;
            padding: 3rem 2rem;
            background: rgba(15, 20, 50, 0.85);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            margin: 2rem 0;
        ">
            <h3 style="color: #00D4FF; margin: 0;">Portfolio is Empty</h3>
            <p style="color: #78909C; margin: 0.5rem 0 0 0;">
                Use the form above to add stocks and start tracking.
            </p>
        </div>
        """)
        return

    # KPI Cards
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_html(
            gradient_card("Total Investment", format_currency(summary['total_investment']),
                          "linear-gradient(135deg, #00D4FF 0%, #0091EA 100%)", "💰")
        )
    with col2:
        render_html(
            gradient_card("Current Value", format_currency(summary['current_value']),
                          "linear-gradient(135deg, #00C853 0%, #00B4D8 100%)", "💵")
        )
    with col3:
        gl = summary['total_gain_loss']
        gl_pct = summary['total_gain_loss_percent']
        grad = "linear-gradient(135deg, #00C853 0%, #38ef7d 100%)" if gl >= 0 else \
               "linear-gradient(135deg, #FF5252 0%, #FF6B6B 100%)"
        render_html(
            gradient_card("P&L", f"{format_currency(gl)} ({gl_pct:+.2f}%)", grad,
                          "📈" if gl >= 0 else "📉")
        )
    with col4:
        render_html(
            gradient_card("Holdings", str(summary['total_stocks']),
                          "linear-gradient(135deg, #FFD740 0%, #FF6B6B 100%)", "🏢")
        )

    st.write("")

    # ── Holdings Table ───────────────────────────────────────
    st.subheader("📋 Holdings")

    if summary['portfolio_details'] is not None:
        details = summary['portfolio_details'].copy()

        # Display table
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
        )

        # Remove buttons
        st.markdown("##### 🗑️ Remove Stock")
        remove_cols = st.columns(min(len(details), 6))
        for idx, (i, row) in enumerate(details.iterrows()):
            with remove_cols[idx % len(remove_cols)]:
                if st.button(f"Remove {row['Ticker']}", key=f"rm_{i}_{row['Ticker']}"):
                    if portfolio_mgr.remove_stock(row['Ticker']):
                        st.success(f"Removed {row['Ticker']}")
                        st.rerun()

    # ── Allocation Chart ─────────────────────────────────────
    st.markdown("---")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📊 Allocation")
        allocation = portfolio_mgr.get_portfolio_allocation()
        if allocation is not None:
            fig = create_portfolio_allocation_chart(allocation)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📈 Portfolio Metrics")
        metrics = calculate_portfolio_metrics(summary)
        if metrics:
            render_html(metric_row("Holdings", str(metrics['num_stocks'])))
            render_html(metric_row("Wtd Avg Gain", f"{metrics['weighted_avg_gain']:.2f}%"))
            render_html(metric_row("Max Allocation", f"{metrics['max_allocation_percent']:.1f}%"))

            risk_color = "#00C853" if "Low" in metrics['risk_level'] else "#FFD740" if "Moderate" in metrics['risk_level'] else "#FF5252"
            render_html(metric_row("Risk Level", metrics['risk_level'], risk_color))

    # ── Export ───────────────────────────────────────────────
    if summary['portfolio_details'] is not None:
        st.markdown("---")
        csv = summary['portfolio_details'].to_csv(index=False)
        st.download_button(
            label="📥 Export Portfolio CSV",
            data=csv,
            file_name=f"portfolio_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

    st.markdown("---")
    st.info("""
    **💡 Tips:**
    - Adding the same stock twice will automatically average the purchase price
    - Diversify across sectors for better risk management
    - Use **🤖 AI Intelligence** for stock recommendations
    """)

