"""
News & Sentiment Analysis Page
Display news and analyze market sentiment
"""

import streamlit as st
from utils.news import get_cached_news
from utils.sentiment import SentimentAnalyzer
from utils.charts import create_sentiment_chart
from datetime import datetime

def show():
    """Display news and sentiment page"""
    
    st.markdown("""
        <h1 style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📰 News & Sentiment Analysis</h1>
        <p style='font-size: 1.1rem; color: #6b7280;'>Stay updated with latest news and market sentiment</p>
    """, unsafe_allow_html=True)
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        ticker = st.text_input(
            "Enter Stock Ticker",
            value="AAPL",
            help="e.g., AAPL, TSLA, GOOGL"
        ).upper()
    
    with col2:
        days_back = st.selectbox(
            "News Period",
            [7, 14, 30],
            format_func=lambda x: f"Last {x} days"
        )
    
    fetch_button = st.button("📰 Fetch News", type="primary")
    
    if fetch_button or 'news_data' in st.session_state:
        if fetch_button:
            # Fetch news
            with st.spinner("Loading latest news..."):
                articles = get_cached_news(ticker, days_back)
                
                if not articles:
                    st.warning("No news articles found. Using sample data.")
                
                # Analyze sentiment
                analyzer = SentimentAnalyzer()
                sentiment_results = analyzer.analyze_news_articles(articles)
                recommendation = analyzer.get_sentiment_recommendation(sentiment_results)
            
            # Store in session state
            st.session_state.news_data = {
                'ticker': ticker,
                'articles': articles,
                'sentiment': sentiment_results,
                'recommendation': recommendation
            }
        
        # Retrieve from session state
        data = st.session_state.news_data
        ticker = data['ticker']
        articles = data['articles']
        sentiment_results = data['sentiment']
        recommendation = data['recommendation']
        
        # Sentiment overview
        st.markdown("---")
        st.header(f"📊 Sentiment Overview for {ticker}")
        
        if sentiment_results:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Sentiment metrics
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric(
                        "Overall Sentiment",
                        sentiment_results['overall_sentiment']
                    )
                
                with col_b:
                    st.metric(
                        "Positive",
                        f"{sentiment_results['positive_percent']:.1f}%"
                    )
                
                with col_c:
                    st.metric(
                        "Negative",
                        f"{sentiment_results['negative_percent']:.1f}%"
                    )
                
                # Recommendation
                if recommendation:
                    st.markdown("---")
                    st.markdown(f"### 🎯 Market Outlook: {recommendation['recommendation']}")
                    st.markdown(f"**{recommendation['message']}**")
            
            with col2:
                # Sentiment chart
                fig = create_sentiment_chart(sentiment_results)
                st.plotly_chart(fig, use_container_width=True)
        
        # News articles
        st.markdown("---")
        st.header("📰 Latest News Articles")
        
        if articles:
            for i, article in enumerate(articles[:10]):  # Show top 10
                with st.expander(
                    f"📄 {article.get('title', 'No title')}",
                    expanded=(i == 0)
                ):
                    # Article details
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        # Description
                        description = article.get('description', 'No description available')
                        st.write(description)
                        
                        # Link
                        url = article.get('url', '#')
                        if url != '#':
                            st.markdown(f"[Read full article]({url})")
                    
                    with col2:
                        # Source and date
                        source = article.get('source', {}).get('name', 'Unknown')
                        st.write(f"**Source:** {source}")
                        
                        published = article.get('publishedAt', '')
                        if published:
                            try:
                                pub_date = datetime.fromisoformat(published.replace('Z', '+00:00'))
                                st.write(f"**Date:** {pub_date.strftime('%Y-%m-%d')}")
                            except:
                                st.write(f"**Date:** {published[:10]}")
                    
                    # Analyze individual article sentiment
                    analyzer = SentimentAnalyzer()
                    text = f"{article.get('title', '')} {article.get('description', '')}"
                    article_sentiment = analyzer.analyze_text(text)
                    
                    if article_sentiment:
                        sentiment = article_sentiment['sentiment']
                        polarity = article_sentiment['polarity']
                        
                        if sentiment == 'Positive':
                            st.success(f"Sentiment: {sentiment} (Score: {polarity:.2f})")
                        elif sentiment == 'Negative':
                            st.error(f"Sentiment: {sentiment} (Score: {polarity:.2f})")
                        else:
                            st.info(f"Sentiment: {sentiment} (Score: {polarity:.2f})")
        else:
            st.info("No news articles available at the moment.")
        
        # Setup instructions
        st.markdown("---")
        st.header("🔧 Setup News API")
        
        with st.expander("ℹ️ How to get more news articles"):
            st.markdown("""
            This application uses NewsAPI to fetch real-time news. To get access:
            
            1. Go to [https://newsapi.org/](https://newsapi.org/)
            2. Sign up for a free API key
            3. Open `config.py` file
            4. Replace `YOUR_API_KEY_HERE` with your actual API key
            5. Restart the application
            
            **Free tier includes:**
            - 100 requests per day
            - Access to headlines and articles
            - Multiple news sources
            
            Without an API key, the app will show sample news data.
            """)
        
        # Important note
        st.info("""
        **📌 Note:** Sentiment analysis is based on natural language processing and may not
        always accurately reflect the true market sentiment. Use it as one of many tools for
        investment research, not as the sole basis for decisions.
        """)
