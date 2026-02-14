"""
Portfolio Tracker Page
Track and manage your stock portfolio
"""

import streamlit as st
import pandas as pd
from utils.portfolio import PortfolioManager, calculate_portfolio_metrics
from utils.charts import create_portfolio_allocation_chart
from utils.stock_data import format_currency, format_large_number
from utils.news import NewsFetcher
from datetime import datetime

def show():
    """Display portfolio tracker page"""
    
    st.markdown("""
        <h1 style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>💼 My Portfolio</h1>
        <p style='font-size: 1.1rem; color: #6b7280;'>Track your investments and monitor performance</p>
    """, unsafe_allow_html=True)
    
    # Initialize portfolio manager
    portfolio_mgr = PortfolioManager()
    
    # Add Stock Section (on main screen)
    st.markdown("---")
    st.header("➕ Add Stock to Portfolio")
    
    with st.form("add_stock_form"):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            new_ticker = st.text_input("Ticker Symbol", help="e.g., AAPL, TSLA, RELIANCE.NS").upper()
        
        with col2:
            quantity = st.number_input("Quantity", min_value=0.01, value=1.0, step=0.01)
        
        with col3:
            purchase_price = st.number_input("Purchase Price (₹)", min_value=0.01, value=100.0, step=0.01)
        
        with col4:
            purchase_date = st.date_input("Purchase Date")
        
        submit_button = st.form_submit_button("Add to Portfolio", type="primary")
        
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
                    st.error("Failed to add stock. Please check the ticker symbol.")
            else:
                st.error("Please enter a ticker symbol")
    
    # Get portfolio summary
    summary = portfolio_mgr.get_portfolio_summary()
    
    if summary['total_stocks'] == 0:
        st.info("""
        👋 Your portfolio is empty! 
        
        Use the form above to add stocks to your portfolio and start tracking your investments.
        """)
        return
    
    # Portfolio overview
    st.markdown("---")
    st.header("📊 Portfolio Overview")
    
    # Highlight Total Investment and Current Value prominently
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white; margin: 0;'>💰 Total Investment</h3>
                <h1 style='color: white; margin: 10px 0; font-size: 2.5rem;'>{}</h1>
            </div>
        """.format(format_currency(summary['total_investment'])), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white; margin: 0;'>💵 Current Value</h3>
                <h1 style='color: white; margin: 10px 0; font-size: 2.5rem;'>{}</h1>
            </div>
        """.format(format_currency(summary['current_value'])), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
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
        
        # Column headers
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([1.2, 1.5, 0.8, 1, 1, 1.2, 1, 1, 1, 0.6])
        with col1:
            st.write("**Ticker**")
        with col2:
            st.write("**Company**")
        with col3:
            st.write("**Qty**")
        with col4:
            st.write("**Buy Price**")
        with col5:
            st.write("**Current**")
        with col6:
            st.write("**Investment**")
        with col7:
            st.write("**Value**")
        with col8:
            st.write("**Gain/Loss**")
        with col9:
            st.write("**%**")
        with col10:
            st.write("**Action**")
        
        st.markdown("---")
        
        # Display each stock with delete option
        for idx, row in details.iterrows():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([1.2, 1.5, 0.8, 1, 1, 1.2, 1, 1, 1, 0.6])
            
            with col1:
                st.write(f"**{row['Ticker']}**")
            with col2:
                company_name = row['Company_Name'][:20] + "..." if len(row['Company_Name']) > 20 else row['Company_Name']
                st.write(company_name)
            with col3:
                st.write(f"{row['Quantity']:.2f}")
            with col4:
                st.write(f"{format_currency(row['Purchase_Price'])}")
            with col5:
                st.write(f"{format_currency(row['Current_Price'])}")
            with col6:
                st.write(f"{format_currency(row['Investment'])}")
            with col7:
                st.write(f"{format_currency(row['Current_Value'])}")
            with col8:
                st.write(f"{format_currency(row['Gain_Loss'])}")
            with col9:
                gain_color = "🟢" if row['Gain_Loss_Percent'] >= 0 else "🔴"
                st.write(f"{gain_color} {row['Gain_Loss_Percent']:.2f}%")
            with col10:
                if st.button("🗑️", key=f"delete_{idx}_{row['Ticker']}", help=f"Remove {row['Ticker']} from portfolio"):
                    if portfolio_mgr.remove_stock(row['Ticker']):
                        st.success(f"✅ Removed {row['Ticker']} from portfolio!")
                        st.rerun()
    
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
    
    # Latest News for Each Stock
    st.markdown("---")
    st.header("📰 Latest News for Portfolio Stocks")
    
    news_fetcher = NewsFetcher()
    
    if summary['portfolio_details'] is not None:
        stock_list = summary['portfolio_details']['Ticker'].tolist()
        
        for ticker in stock_list:
            with st.expander(f"📊 {ticker} - Latest News", expanded=True):
                try:
                    # Fetch only 1 latest news article
                    articles = news_fetcher.fetch_stock_news(ticker, days_back=7, max_articles=1)
                    
                    if articles and len(articles) > 0:
                        article = articles[0]
                        
                        # Display article
                        st.markdown(f"### [{article.get('title', 'No title')}]({article.get('url', '#')})")
                        st.write(f"**Source:** {article.get('source', {}).get('name', 'Unknown')}")
                        
                        # Format published date
                        published = article.get('publishedAt', '')
                        if published:
                            try:
                                pub_date = datetime.fromisoformat(published.replace('Z', '+00:00'))
                                st.write(f"**Published:** {pub_date.strftime('%B %d, %Y at %I:%M %p')}")
                            except:
                                st.write(f"**Published:** {published}")
                        
                        # Description
                        description = article.get('description', 'No description available')
                        if description:
                            st.write(description)
                        
                        # Read more link
                        if article.get('url') and article.get('url') != '#':
                            st.markdown(f"[Read More →]({article.get('url')})")
                    else:
                        st.info(f"No recent news available for {ticker}")
                
                except Exception as e:
                    st.warning(f"Unable to fetch news for {ticker}: {str(e)}")
    
    # Tips
    st.markdown("---")
    st.info("""
    **💡 Portfolio Tips:**
    - When you add the same stock twice, it automatically averages the purchase price
    - Use the 🗑️ button to remove stocks from your portfolio
    - Diversify across different sectors for better risk management
    - Regular portfolio rebalancing is recommended
    - Monitor your allocation percentages
    - Review performance metrics regularly
    - Stay updated with latest news for your stocks
    """)
