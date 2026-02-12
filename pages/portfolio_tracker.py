"""
Portfolio Tracker Page
Track and manage your stock portfolio
"""

import streamlit as st
import pandas as pd
from utils.portfolio import PortfolioManager, calculate_portfolio_metrics
from utils.charts import create_portfolio_allocation_chart
from utils.stock_data import format_currency, format_large_number

def show():
    """Display portfolio tracker page"""
    
    st.markdown("""
        <h1 style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>💼 Portfolio Tracker</h1>
        <p style='font-size: 1.1rem; color: #6b7280;'>Track your investments and monitor performance</p>
    """, unsafe_allow_html=True)
    
    # Initialize portfolio manager
    portfolio_mgr = PortfolioManager()
    
    # Sidebar for adding stocks
    with st.sidebar:
        st.header("➕ Add Stock to Portfolio")
        
        with st.form("add_stock_form"):
            new_ticker = st.text_input("Ticker Symbol", help="e.g., AAPL, TSLA").upper()
            quantity = st.number_input("Quantity", min_value=0.01, value=1.0, step=0.01)
            purchase_price = st.number_input("Purchase Price (₹)", min_value=0.01, value=100.0, step=0.01)
            purchase_date = st.date_input("Purchase Date")
            
            submit_button = st.form_submit_button("Add to Portfolio")
            
            if submit_button:
                if new_ticker:
                    success = portfolio_mgr.add_stock(
                        new_ticker,
                        quantity,
                        purchase_price,
                        purchase_date.strftime('%Y-%m-%d')
                    )
                    if success:
                        st.success(f"✅ Added {new_ticker} to portfolio!")
                        st.rerun()
                    else:
                        st.error("Failed to add stock")
                else:
                    st.error("Please enter a ticker symbol")
    
    # Get portfolio summary
    summary = portfolio_mgr.get_portfolio_summary()
    
    if summary['total_stocks'] == 0:
        st.info("""
        👋 Your portfolio is empty! 
        
        Use the sidebar to add stocks to your portfolio and start tracking your investments.
        """)
        return
    
    # Portfolio overview
    st.markdown("---")
    st.header("📊 Portfolio Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Investment",
            format_currency(summary['total_investment'])
        )
    
    with col2:
        st.metric(
            "Current Value",
            format_currency(summary['current_value'])
        )
    
    with col3:
        gain_loss = summary['total_gain_loss']
        gain_loss_pct = summary['total_gain_loss_percent']
        st.metric(
            "Total Gain/Loss",
            format_currency(gain_loss),
            f"{gain_loss_pct:+.2f}%"
        )
    
    with col4:
        st.metric(
            "Number of Stocks",
            summary['total_stocks']
        )
    
    # Portfolio allocation
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Portfolio Allocation")
        allocation = portfolio_mgr.get_portfolio_allocation()
        if allocation is not None:
            fig = create_portfolio_allocation_chart(allocation)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏆 Best & Worst Performers")
        performers = portfolio_mgr.get_best_worst_performers()
        
        if performers:
            # Best performer
            st.markdown("**🟢 Best Performer**")
            best = performers['best']
            st.write(f"**{best['ticker']}** - {best['company']}")
            st.write(f"Gain: {format_currency(best['gain_loss'])} ({best['gain_loss_percent']:.2f}%)")
            
            st.markdown("---")
            
            # Worst performer
            st.markdown("**🔴 Worst Performer**")
            worst = performers['worst']
            st.write(f"**{worst['ticker']}** - {worst['company']}")
            st.write(f"Loss: {format_currency(worst['gain_loss'])} ({worst['gain_loss_percent']:.2f}%)")
    
    # Portfolio details
    st.markdown("---")
    st.header("📋 Portfolio Details")
    
    if summary['portfolio_details'] is not None:
        details = summary['portfolio_details'].copy()
        
        # Format columns for display
        details['Purchase_Price'] = details['Purchase_Price'].apply(lambda x: f"${x:.2f}")
        details['Current_Price'] = details['Current_Price'].apply(lambda x: f"${x:.2f}")
        details['Investment'] = details['Investment'].apply(lambda x: f"${x:,.2f}")
        details['Current_Value'] = details['Current_Value'].apply(lambda x: f"${x:,.2f}")
        details['Gain_Loss'] = details['Gain_Loss'].apply(lambda x: f"${x:,.2f}")
        details['Gain_Loss_Percent'] = details['Gain_Loss_Percent'].apply(lambda x: f"{x:.2f}%")
        
        # Rename columns
        details.columns = [
            'Ticker', 'Company', 'Quantity', 'Purchase Price', 'Current Price',
            'Purchase Date', 'Investment', 'Current Value', 'Gain/Loss', 'Gain/Loss %'
        ]
        
        st.dataframe(details, use_container_width=True, hide_index=True)
    
    # Portfolio metrics
    st.markdown("---")
    st.header("📈 Portfolio Metrics")
    
    metrics = calculate_portfolio_metrics(summary)
    if metrics:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Number of Holdings", metrics['num_stocks'])
        
        with col2:
            st.metric("Weighted Avg Gain", f"{metrics['weighted_avg_gain']:.2f}%")
        
        with col3:
            st.metric("Max Allocation", f"{metrics['max_allocation_percent']:.2f}%")
        
        # Risk level
        risk_color = "green" if "Low" in metrics['risk_level'] else "orange" if "Moderate" in metrics['risk_level'] else "red"
        st.markdown(f"**Risk Assessment:** :{risk_color}[{metrics['risk_level']}]")
    
    # Management actions
    st.markdown("---")
    st.header("⚙️ Portfolio Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Portfolio", type="secondary"):
            if st.checkbox("Confirm deletion"):
                if portfolio_mgr.clear_portfolio():
                    st.success("Portfolio cleared!")
                    st.rerun()
    
    with col2:
        if st.button("📥 Export Portfolio", type="secondary"):
            from utils.portfolio import export_portfolio_report
            if export_portfolio_report(summary, "my_portfolio.csv"):
                st.success("Portfolio exported to my_portfolio.csv")
    
    # Tips
    st.markdown("---")
    st.info("""
    **💡 Portfolio Tips:**
    - Diversify across different sectors
    - Regular portfolio rebalancing recommended
    - Monitor your allocation percentages
    - Review performance metrics regularly
    """)
