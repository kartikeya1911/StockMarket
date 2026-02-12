"""
Custom Dashboard Page
Create your own stock watchlist and view analytics
"""

import streamlit as st
import pandas as pd
import json
import os
from utils.stock_data import StockDataFetcher, format_large_number, format_currency
from utils.portfolio import PortfolioManager
from utils.charts import create_portfolio_allocation_chart
import plotly.graph_objects as go
import plotly.express as px

# Dashboard data file
DASHBOARD_FILE = "data/watchlist.json"

def load_watchlist():
    """Load watchlist from file"""
    if os.path.exists(DASHBOARD_FILE):
        try:
            with open(DASHBOARD_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_watchlist(watchlist):
    """Save watchlist to file"""
    os.makedirs(os.path.dirname(DASHBOARD_FILE), exist_ok=True)
    with open(DASHBOARD_FILE, 'w') as f:
        json.dump(watchlist, f)

def show():
    """Display custom dashboard page"""
    
    st.markdown("""
        <h1 style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📊 My Stock Dashboard</h1>
        <p style='font-size: 1.1rem; color: #6b7280;'>Create your personalized stock watchlist and analytics</p>
    """, unsafe_allow_html=True)
    
    # Load watchlist
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = load_watchlist()
    
    # Initialize portfolio manager
    portfolio_mgr = PortfolioManager()
    
    # Sidebar with tabs for Watchlist and Portfolio
    st.sidebar.markdown("### 📊 Dashboard Controls")
    
    sidebar_tab = st.sidebar.radio(
        "Select Action:",
        ["➕ Add to Watchlist", "💼 Add to Portfolio"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    if sidebar_tab == "➕ Add to Watchlist":
        st.sidebar.markdown("#### Add Stock to Watchlist")
        with st.sidebar.form("add_watchlist_form"):
            new_ticker = st.text_input(
                "Stock Ticker", 
                placeholder="e.g., RELIANCE.NS, TCS.NS",
                help="Enter stock ticker symbol"
            ).upper()
            
            add_button = st.form_submit_button("Add to Watchlist", use_container_width=True)
            
            if add_button and new_ticker:
                # Validate ticker
                fetcher = StockDataFetcher(new_ticker)
                if fetcher.validate_ticker():
                    if new_ticker not in st.session_state.watchlist:
                        st.session_state.watchlist.append(new_ticker)
                        save_watchlist(st.session_state.watchlist)
                        st.sidebar.success(f"✅ Added {new_ticker}")
                        st.rerun()
                    else:
                        st.sidebar.warning(f"⚠️ {new_ticker} already in watchlist")
                else:
                    st.sidebar.error("❌ Invalid ticker symbol")
    
    else:  # Add to Portfolio
        st.sidebar.markdown("#### Add Stock to Portfolio")
        with st.sidebar.form("add_portfolio_form"):
            portfolio_ticker = st.text_input(
                "Ticker Symbol",
                placeholder="e.g., RELIANCE.NS",
                help="Enter stock ticker symbol"
            ).upper()
            quantity = st.number_input("Quantity", min_value=0.01, value=1.0, step=0.01)
            purchase_price = st.number_input("Purchase Price (₹)", min_value=0.01, value=100.0, step=0.01)
            purchase_date = st.date_input("Purchase Date")
            
            portfolio_button = st.form_submit_button("Add to Portfolio", use_container_width=True)
            
            if portfolio_button and portfolio_ticker:
                success = portfolio_mgr.add_stock(
                    portfolio_ticker,
                    quantity,
                    purchase_price,
                    purchase_date.strftime('%Y-%m-%d')
                )
                if success:
                    st.sidebar.success(f"✅ Added {portfolio_ticker} to portfolio!")
                    st.rerun()
                else:
                    st.sidebar.error("❌ Failed to add stock")
    
    # Manage watchlist and portfolio
    st.sidebar.markdown("---")
    
    view_option = st.sidebar.selectbox(
        "View:",
        ["📋 Watchlist", "💼 Portfolio", "📊 Both"]
    )
    
    if view_option in ["📋 Watchlist", "📊 Both"]:
        if st.session_state.watchlist:
            st.sidebar.markdown("#### Your Watchlist")
            for ticker in st.session_state.watchlist:
                col1, col2 = st.sidebar.columns([3, 1])
                with col1:
                    st.write(f"• {ticker}")
                with col2:
                    if st.button("🗑️", key=f"del_watch_{ticker}"):
                        st.session_state.watchlist.remove(ticker)
                        save_watchlist(st.session_state.watchlist)
                        st.rerun()
    
    if view_option in ["💼 Portfolio", "📊 Both"]:
        portfolio_summary = portfolio_mgr.get_portfolio_summary()
        if portfolio_summary['total_stocks'] > 0:
            st.sidebar.markdown("#### Your Portfolio")
            portfolio_data = portfolio_mgr.get_portfolio()
            for _, stock in portfolio_data.iterrows():
                col1, col2 = st.sidebar.columns([3, 1])
                with col1:
                    st.write(f"• {stock['ticker']} ({stock['quantity']})")
                with col2:
                    if st.button("🗑️", key=f"del_port_{stock['ticker']}_{stock['purchase_date']}"):
                        portfolio_mgr.remove_stock(stock['ticker'], stock['purchase_date'])
                        st.rerun()
    
    # Main dashboard
    portfolio_summary = portfolio_mgr.get_portfolio_summary()
    has_watchlist = len(st.session_state.watchlist) > 0
    has_portfolio = portfolio_summary['total_stocks'] > 0
    
    if not has_watchlist and not has_portfolio:
        st.info("""
        👋 **Welcome to Your Stock Dashboard!**
        
        Get started by adding stocks to your watchlist or portfolio using the sidebar.
        
        **Steps:**
        1. Select "➕ Add to Watchlist" or "💼 Add to Portfolio" in the sidebar
        2. Enter a stock ticker
        3. View comprehensive analytics and charts
        
        **Popular Indian Stocks:** RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS, ICICIBANK.NS
        """)
        return
    
    # Show Portfolio Overview if portfolio view is selected
    if view_option in ["💼 Portfolio", "📊 Both"] and has_portfolio:
        st.markdown("---")
        st.header("💼 Portfolio Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Investment",
                format_currency(portfolio_summary['total_investment'])
            )
        
        with col2:
            st.metric(
                "Current Value",
                format_currency(portfolio_summary['current_value'])
            )
        
        with col3:
            gain_loss = portfolio_summary['total_gain_loss']
            gain_loss_pct = portfolio_summary['total_gain_loss_percent']
            st.metric(
                "Total Gain/Loss",
                format_currency(gain_loss),
                f"{gain_loss_pct:+.2f}%"
            )
        
        with col4:
            st.metric(
                "Portfolio Stocks",
                portfolio_summary['total_stocks']
            )
        
        # Portfolio allocation
        if portfolio_summary['total_stocks'] > 0:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("💰 Portfolio Value Distribution")
                portfolio_data = portfolio_mgr.get_portfolio()
                fig = create_portfolio_allocation_chart(portfolio_data)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("📊 Best & Worst Performers")
                sorted_portfolio = portfolio_data.sort_values('gain_loss_percent', ascending=False)
                
                if len(sorted_portfolio) > 0:
                    best = sorted_portfolio.iloc[0]
                    st.success(f"""
                    **🔥 Best:** {best['ticker']}  
                    Gain: {format_currency(best['gain_loss'])} ({best['gain_loss_percent']:+.2f}%)
                    """)
                    
                    if len(sorted_portfolio) > 1:
                        worst = sorted_portfolio.iloc[-1]
                        color = "error" if worst['gain_loss'] < 0 else "info"
                        getattr(st, color)(f"""
                        **📉 Worst:** {worst['ticker']}  
                        Gain/Loss: {format_currency(worst['gain_loss'])} ({worst['gain_loss_percent']:+.2f}%)
                        """)
    
    # Show Watchlist if watchlist view is selected
    if view_option in ["📋 Watchlist", "📊 Both"] and has_watchlist:
        # Fetch data for all stocks
        with st.spinner("📊 Loading your watchlist data..."):
            stocks_data = []
            
            for ticker in st.session_state.watchlist:
                fetcher = StockDataFetcher(ticker)
                stock_info = fetcher.get_stock_info()
                
                if stock_info:
                    stocks_data.append({
                        'Ticker': ticker,
                        'Name': stock_info['name'],
                        'Price': stock_info['current_price'],
                        'Change': ((stock_info['current_price'] - stock_info['previous_close']) / 
                                  stock_info['previous_close'] * 100) if stock_info['previous_close'] else 0,
                        'Market Cap': stock_info['market_cap'],
                        'Volume': stock_info['volume'],
                        'PE Ratio': stock_info['pe_ratio'],
                        'Sector': stock_info['sector'],
                        '52W High': stock_info['52_week_high'],
                        '52W Low': stock_info['52_week_low']
                    })
        
        if not stocks_data:
            st.error("Unable to fetch data for your stocks. Please try again.")
            return
        
        df = pd.DataFrame(stocks_data)
        
        # Summary metrics
        st.markdown("---")
        st.header("📈 Watchlist Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Stocks", len(df))
        
        with col2:
            avg_change = df['Change'].mean()
            st.metric(
                "Avg Change",
                f"{avg_change:+.2f}%",
                delta=f"{avg_change:.2f}%"
            )
        
        with col3:
            total_market_cap = df['Market Cap'].sum()
            st.metric("Total Market Cap", format_large_number(total_market_cap))
        
        with col4:
            gainers = len(df[df['Change'] > 0])
            st.metric("Gainers", f"{gainers}/{len(df)}")
        
        # Stock cards
        st.markdown("---")
        st.header("💼 Your Stocks")
        
        # Create cards for each stock
        for idx, row in df.iterrows():
            with st.expander(f"📊 {row['Ticker']} - {row['Name']}", expanded=(idx == 0)):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Current Price",
                        format_currency(row['Price']),
                        f"{row['Change']:+.2f}%"
                    )
                
                with col2:
                    st.metric("Market Cap", format_large_number(row['Market Cap']))
                
                with col3:
                    pe = row['PE Ratio']
                    st.metric("PE Ratio", f"{pe:.2f}" if pe and pe != 0 else "N/A")
                
                with col4:
                    st.metric("Sector", row['Sector'])
                
                # Additional details
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Volume:** {format_large_number(row['Volume'])}")
                with col2:
                    st.write(f"**52W High:** {format_currency(row['52W High'])}")
                with col3:
                    st.write(f"**52W Low:** {format_currency(row['52W Low'])}")
        
        # Visualizations
        st.markdown("---")
        st.header("📊 Visual Analytics")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Market Cap", "Sectors", "Performance", "PE Ratios"])
        
        with tab1:
            st.subheader("Market Cap Distribution")
            # Market cap pie chart
            fig = px.pie(
                df,
                values='Market Cap',
                names='Ticker',
                title='Market Capitalization Distribution',
                hole=0.3,
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            
            # Market cap bar chart
            fig2 = px.bar(
                df.sort_values('Market Cap', ascending=True),
                x='Market Cap',
                y='Ticker',
                orientation='h',
                title='Market Cap Comparison',
                color='Market Cap',
                color_continuous_scale='Viridis'
            )
            fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            st.subheader("Sector Distribution")
            # Sector distribution
            sector_counts = df['Sector'].value_counts()
            
            fig = px.pie(
                values=sector_counts.values,
                names=sector_counts.index,
                title='Sector Allocation',
                hole=0.3,
                color_discrete_sequence=px.colors.sequential.Plasma
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            
            # Sector table
            st.markdown("#### Sector Breakdown")
            sector_df = df.groupby('Sector').agg({
                'Ticker': 'count',
                'Market Cap': 'sum',
                'Change': 'mean'
            }).reset_index()
            sector_df.columns = ['Sector', 'Count', 'Total Market Cap', 'Avg Change %']
            sector_df['Total Market Cap'] = sector_df['Total Market Cap'].apply(format_large_number)
            sector_df['Avg Change %'] = sector_df['Avg Change %'].apply(lambda x: f"{x:.2f}%")
            st.dataframe(sector_df, use_container_width=True, hide_index=True)
        
        with tab3:
            st.subheader("Price Performance")
            # Performance chart
            colors = ['green' if x > 0 else 'red' for x in df['Change']]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=df['Ticker'],
                    y=df['Change'],
                    marker_color=colors,
                    text=df['Change'].apply(lambda x: f"{x:.2f}%"),
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title='Daily Performance (%)',
                xaxis_title='Stock',
                yaxis_title='Change %',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Performance stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Best Performer", df.loc[df['Change'].idxmax(), 'Ticker'], 
                         f"+{df['Change'].max():.2f}%")
            with col2:
                st.metric("Worst Performer", df.loc[df['Change'].idxmin(), 'Ticker'], 
                         f"{df['Change'].min():.2f}%")
            with col3:
                positive = len(df[df['Change'] > 0])
                st.metric("Win Rate", f"{(positive/len(df)*100):.1f}%")
        
        with tab4:
            st.subheader("PE Ratio Analysis")
            # Filter out N/A PE ratios
            df_pe = df[df['PE Ratio'] > 0].copy()
            
            if len(df_pe) > 0:
                # PE ratio chart
                fig = px.bar(
                    df_pe.sort_values('PE Ratio'),
                    x='PE Ratio',
                    y='Ticker',
                    orientation='h',
                    title='Price to Earnings Ratio Comparison',
                    color='PE Ratio',
                    color_continuous_scale='RdYlGn_r'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # PE statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average PE", f"{df_pe['PE Ratio'].mean():.2f}")
                with col2:
                    st.metric("Highest PE", f"{df_pe['PE Ratio'].max():.2f}")
                with col3:
                    st.metric("Lowest PE", f"{df_pe['PE Ratio'].min():.2f}")
            else:
                st.info("No PE ratio data available for the stocks in your watchlist.")
        
        # Data table
        st.markdown("---")
        st.header("📋 Detailed Data Table")
        
        # Format data for display
        display_df = df.copy()
        display_df['Price'] = display_df['Price'].apply(lambda x: format_currency(x))
        display_df['Change'] = display_df['Change'].apply(lambda x: f"{x:+.2f}%")
        display_df['Market Cap'] = display_df['Market Cap'].apply(format_large_number)
        display_df['Volume'] = display_df['Volume'].apply(format_large_number)
        display_df['PE Ratio'] = display_df['PE Ratio'].apply(lambda x: f"{x:.2f}" if x and x != 0 else "N/A")
        display_df['52W High'] = display_df['52W High'].apply(lambda x: format_currency(x))
        display_df['52W Low'] = display_df['52W Low'].apply(lambda x: format_currency(x))
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Export option
        if st.button("📥 Export to CSV", type="secondary"):
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="my_watchlist.csv",
                mime="text/csv"
            )
    
    # Tips
    st.markdown("---")
    st.info(f"""
    **💡 Dashboard Tips:**
    - Switch between **Watchlist**, **Portfolio**, or **Both** views using the sidebar dropdown
    - Add stocks to watchlist for quick monitoring without tracking purchases
    - Add stocks to portfolio to track your actual investments and P&L
    - Use the visualizations to identify sector concentration and performance trends
    - Export your data for further analysis
    - Remove stocks by clicking the 🗑️ button in the sidebar
    """)
