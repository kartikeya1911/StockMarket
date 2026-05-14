"""
News & Sentiment Analysis Page — News feed with AI sentiment scoring.
"""

import streamlit as st
from utils.news import get_cached_news
from utils.sentiment import SentimentAnalyzer
from utils.charts import create_sentiment_chart
from styles.theme import page_header, glass_card, metric_row, signal_badge, render_html
from datetime import datetime


def show():
    """Display the news and sentiment page."""

    page_header("News & Sentiment", "Real-time news with AI sentiment analysis", "📰")

    # ── Inputs ───────────────────────────────────────────────
    col1, col2 = st.columns([2, 1])
    with col1:
        ticker = st.text_input("Enter Stock Ticker", value="AAPL",
                               help="e.g., AAPL, TSLA, GOOGL").upper()
    with col2:
        days_back = st.selectbox("Period", [7, 14, 30],
                                 format_func=lambda x: f"Last {x} days")

    fetch_btn = st.button("📰 Fetch News", type="primary", use_container_width=True)

    if fetch_btn or 'news_result' in st.session_state:
        if fetch_btn:
            with st.spinner("Loading latest news..."):
                articles = get_cached_news(ticker, days_back)
                if not articles:
                    st.warning("No news articles found. Showing sample data.")

                analyzer = SentimentAnalyzer()
                sentiment_results = analyzer.analyze_news_articles(articles)
                recommendation = analyzer.get_sentiment_recommendation(sentiment_results)

            st.session_state.news_result = {
                'ticker': ticker,
                'articles': articles,
                'sentiment': sentiment_results,
                'recommendation': recommendation,
            }

        data = st.session_state.news_result
        ticker = data['ticker']
        articles = data['articles']
        sentiment_results = data['sentiment']
        recommendation = data['recommendation']

        # ── Sentiment Overview ───────────────────────────────
        st.markdown("---")
        st.subheader(f"📊 Sentiment Overview — {ticker}")

        if sentiment_results:
            col1, col2 = st.columns([1, 1])

            with col1:
                # Metrics
                c1, c2, c3 = st.columns(3)
                with c1:
                    overall = sentiment_results['overall_sentiment']
                    color = "#00C853" if overall == "Positive" else "#FF5252" if overall == "Negative" else "#FFD740"
                    st.metric("Overall", overall)
                with c2:
                    st.metric("Positive", f"{sentiment_results['positive_percent']:.0f}%")
                with c3:
                    st.metric("Negative", f"{sentiment_results['negative_percent']:.0f}%")

                # Recommendation
                if recommendation:
                    rec = recommendation['recommendation']
                    rec_color_map = {
                        'Bullish': '#00C853', 'Moderately Bullish': '#00B4D8',
                        'Bearish': '#FF5252', 'Moderately Bearish': '#FFD740',
                        'Neutral': '#78909C',
                    }
                    rec_color = rec_color_map.get(rec, '#78909C')

                    render_html(f"""
                    <div style="
                        background: {rec_color}15;
                        border: 1px solid {rec_color}44;
                        border-radius: 12px;
                        padding: 1rem;
                        text-align: center;
                        margin: 0.5rem 0;
                    ">
                        <p style="color: #78909C; margin: 0; font-size: 0.8rem;">Market Outlook</p>
                        <h3 style="color: {rec_color}; margin: 0.2rem 0;">{rec}</h3>
                        <p style="color: #E8EAF6; margin: 0; font-size: 0.85rem;">{recommendation['message']}</p>
                    </div>
                    """)

            with col2:
                fig = create_sentiment_chart(sentiment_results)
                st.plotly_chart(fig, use_container_width=True)

        # ── News Articles ────────────────────────────────────
        st.markdown("---")
        st.subheader("📰 Latest Articles")

        if articles:
            analyzer = SentimentAnalyzer()

            for i, article in enumerate(articles[:10]):
                title = article.get('title', 'No title')
                url = article.get('url', '#')
                source = article.get('source', {}).get('name', 'Unknown')
                published = article.get('publishedAt', '')
                desc = article.get('description', '') or ''

                # Analyze sentiment
                text = f"{title} {desc}"
                article_sent = analyzer.analyze_text(text)

                # Format date
                date_str = ""
                if published:
                    try:
                        pub_date = datetime.fromisoformat(published.replace('Z', '+00:00'))
                        date_str = pub_date.strftime('%b %d, %Y')
                    except Exception:
                        date_str = published[:10]

                with st.expander(f"{'📄'} {title}", expanded=(i == 0)):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if desc:
                            st.write(desc[:300] + "..." if len(desc) > 300 else desc)
                        if url != '#':
                            st.markdown(f"[Read full article →]({url})")
                    with col2:
                        st.caption(f"**Source:** {source}")
                        if date_str:
                            st.caption(f"**Date:** {date_str}")

                        if article_sent:
                            sent = article_sent['sentiment']
                            pol = article_sent['polarity']
                            color = "#00C853" if sent == 'Positive' else "#FF5252" if sent == 'Negative' else "#78909C"
                            render_html(signal_badge(f"{sent} ({pol:+.2f})", color))
        else:
            st.info("No news articles available.")

        # ── Setup ────────────────────────────────────────────
        with st.expander("🔧 Setup News API"):
            st.markdown("""
            This app uses [NewsAPI.org](https://newsapi.org/) for real-time news.

            1. Sign up for a free API key at [newsapi.org](https://newsapi.org/)
            2. Set the `NEWS_API_KEY` environment variable
            3. Restart the application

            Without a valid key, sample data will be shown.
            """)

        st.markdown("---")
        st.info("""
        **📌 Note:** Sentiment analysis uses NLP algorithms and may not always
        perfectly capture market sentiment. Use alongside other analysis tools.
        """)

