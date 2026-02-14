"""
Portfolio Dashboard Page
Your portfolio overview and latest news
"""

import streamlit as st
import pandas as pd
from utils.stock_data import format_currency, format_large_number
from utils.portfolio import PortfolioManager
from utils.charts import create_portfolio_allocation_chart
from utils.news import NewsFetcher
from datetime import datetime
import plotly.graph_objects as go


def show():
    """Display portfolio dashboard page"""
    
    st.markdown("""
        <h1 style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📊 My Portfolio Dashboard</h1>
        <p style='font-size: 1.1rem; color: #6b7280;'>Track your investments and monitor performance</p>
    """, unsafe_allow_html=True)
    
    # Initialize portfolio manager
    portfolio_mgr = PortfolioManager()
    summary = portfolio_mgr.get_portfolio_summary()
    
    if summary['total_stocks'] == 0:
        st.info("""
        👋 Your portfolio is empty! 
        
        Go to **💼 Portfolio Tracker** to add stocks to your portfolio.
        """)
        return
    
    # Portfolio Overview - Highlight Total Investment and Current Value
    st.markdown("---")
    st.header("💰 Portfolio Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 30px; border-radius: 15px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
                <h3 style='color: white; margin: 0; font-size: 1.2rem;'>💰 Total Investment</h3>
                <h1 style='color: white; margin: 15px 0; font-size: 3rem;'>{}</h1>
            </div>
        """.format(format_currency(summary['total_investment'])), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                        padding: 30px; border-radius: 15px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
                <h3 style='color: white; margin: 0; font-size: 1.2rem;'>💵 Current Value</h3>
                <h1 style='color: white; margin: 15px 0; font-size: 3rem;'>{}</h1>
            </div>
        """.format(format_currency(summary['current_value'])), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gain/Loss and Stock Count
    col3, col4 = st.columns(2)
    
    with col3:
        gain_loss = summary['total_gain_loss']
        gain_loss_pct = summary['total_gain_loss_percent']
        st.metric(
            "📈 Total Gain/Loss",
            format_currency(gain_loss),
            f"{gain_loss_pct:+.2f}%"
        )
    
    with col4:
        st.metric(
            "🏢 Number of Holdings",
            summary['total_stocks']
        )
    
    # Portfolio Holdings Table
    st.markdown("---")
    st.header("📋 My Holdings")
    
    if summary['portfolio_details'] is not None:
        details = summary['portfolio_details'].copy()
        
        # Column headers
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1.2, 1.8, 0.8, 1, 1, 1.2, 1.2, 1, 0.6])
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
            st.write("**Action**")
        
        st.markdown("---")
        
        # Display each stock with delete option
        for idx, row in details.iterrows():
            col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1.2, 1.8, 0.8, 1, 1, 1.2, 1.2, 1, 0.6])
            
            with col1:
                st.write(f"**{row['Ticker']}**")
            with col2:
                company_name = row['Company_Name'][:25] + "..." if len(row['Company_Name']) > 25 else row['Company_Name']
                st.write(company_name)
            with col3:
                st.write(f"{row['Quantity']:.2f}")
            with col4:
                st.write(format_currency(row['Purchase_Price']))
            with col5:
                st.write(format_currency(row['Current_Price']))
            with col6:
                st.write(format_currency(row['Investment']))
            with col7:
                st.write(format_currency(row['Current_Value']))
            with col8:
                gain_color = "🟢" if row['Gain_Loss_Percent'] >= 0 else "🔴"
                st.write(f"{gain_color} {format_currency(row['Gain_Loss'])} ({row['Gain_Loss_Percent']:.2f}%)")
            with col9:
                if st.button("🗑️", key=f"del_dash_{idx}_{row['Ticker']}", help=f"Remove {row['Ticker']}"):
                    if portfolio_mgr.remove_stock(row['Ticker']):
                        st.success(f"✅ Removed {row['Ticker']}!")
                        st.rerun()
    
    # Portfolio Allocation Chart
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
            st.markdown("**🟢 Best Performer**")
            best = performers['best']
            st.write(f"**{best['ticker']}** - {best['company']}")
            st.write(f"Gain: {format_currency(best['gain_loss'])} ({best['gain_loss_percent']:.2f}%)")
            
            st.markdown("---")
            
            st.markdown("**🔴 Worst Performer**")
            worst = performers['worst']
            st.write(f"**{worst['ticker']}** - {worst['company']}")
            st.write(f"Gain/Loss: {format_currency(worst['gain_loss'])} ({worst['gain_loss_percent']:.2f}%)")
    
    # Latest News for Each Stock
    st.markdown("---")
    st.header("📰 Latest News for Your Holdings")
    
    news_fetcher = NewsFetcher()
    
    if summary['portfolio_details'] is not None:
        stock_list = summary['portfolio_details']['Ticker'].tolist()
        
        for ticker in stock_list:
            with st.expander(f"📊 {ticker} - Latest News", expanded=False):
                try:
                    # Fetch only 1 latest news article
                    articles = news_fetcher.fetch_stock_news(ticker, days_back=7, max_articles=1)
                    
                    if articles and len(articles) > 0:
                        article = articles[0]
                        
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
                    st.warning(f"Unable to fetch news for {ticker}")
    
    # Tips
    st.markdown("---")
    st.info("""
    **💡 Dashboard Tips:**
    - Monitor your total investment vs current value at a glance
    - Use 🗑️ button to remove stocks from your portfolio
    - When you buy the same stock multiple times, quantities are added and prices are averaged
    - Check best and worst performers to rebalance your portfolio
    - Stay updated with latest news for each of your holdings
    - Track your portfolio allocation for better diversification
    """)
