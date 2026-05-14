"""
AI Intelligence Page — QuantEdge comprehensive AI-powered stock recommendation
Combines Technical, Fundamental, Sentiment, AI Prediction & Risk analysis.
"""

import streamlit as st
import pandas as pd
from utils.stock_data import StockDataFetcher, format_currency
from utils.indicators import TechnicalIndicators
from utils.charts import create_score_radar, create_risk_gauge
from utils.news import get_cached_news
from utils.sentiment import SentimentAnalyzer
from services.analysis_engine import (
    compute_technical_score,
    compute_fundamental_score,
    compute_risk_score,
    compute_support_resistance,
)
from services.recommendation_engine import generate_recommendation
from models.prediction import create_prediction_pipeline
from styles.theme import (
    page_header, gradient_card, glass_card, section_header,
    recommendation_badge, score_gauge, metric_row, signal_badge, render_html,
)
import config


def show():
    """Display the AI Intelligence page."""

    page_header(
        "AI Intelligence Engine",
        "Institutional-grade analysis with explainable AI recommendations",
        "🤖"
    )

    # ── Input ────────────────────────────────────────────────
    col1, col2 = st.columns([2, 1])
    with col1:
        ticker = st.text_input(
            "Enter Stock Ticker",
            value="AAPL",
            help="e.g., AAPL, TSLA, GOOGL, RELIANCE.NS"
        ).upper()
    with col2:
        period = st.selectbox("Analysis Period", ["1 Year", "2 Years", "5 Years"], index=0)

    analyze = st.button("🚀 Run AI Analysis", type="primary", use_container_width=True)

    if analyze or 'ai_result' in st.session_state:
        if analyze:
            _run_analysis(ticker, period)

        if 'ai_result' not in st.session_state:
            return

        result = st.session_state.ai_result
        rec = result['recommendation']
        ticker = result['ticker']
        current_price = result['current_price']

        # ── Recommendation Header ────────────────────────────
        st.markdown("---")

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            render_html(gradient_card("Current Price", format_currency(current_price),
                                      "linear-gradient(135deg, #00D4FF 0%, #0091EA 100%)", "💰"))
        with col2:
            render_html(recommendation_badge(rec['recommendation']))
        with col3:
            render_html(gradient_card("Confidence", f"{rec['confidence']:.0f}%",
                                      "linear-gradient(135deg, #00C853 0%, #00897B 100%)", "🎯"))

        st.write("")

        # ── Score Breakdown ──────────────────────────────────
        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.subheader("📊 Analysis Scores")
            for dimension, info in rec['breakdown'].items():
                render_html(
                    score_gauge(f"{dimension} ({info['weight']})", info['score'])
                )
            render_html(
                score_gauge("Composite Score", rec['composite_score'])
            )

        with col_right:
            st.subheader("🎯 Score Radar")
            fig = create_score_radar(rec['breakdown'])
            st.plotly_chart(fig, use_container_width=True)

        # ── Explanation ──────────────────────────────────────
        st.markdown("---")
        st.subheader("🧠 AI Reasoning")

        for reason in rec['reasons']:
            render_html(f"""
            <div style="
                background: rgba(15, 20, 50, 0.85);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 10px;
                padding: 0.8rem 1rem;
                margin: 0.4rem 0;
                font-size: 0.88rem;
                color: #E8EAF6;
            ">{reason}</div>
            """)

        # ── Trading Info ─────────────────────────────────────
        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("📍 Entry / Exit Zones")
            if rec.get('entry_zone'):
                render_html(metric_row("Entry Zone", rec['entry_zone'], "#00C853"))
            if rec.get('exit_zone'):
                render_html(metric_row("Exit Zone", rec['exit_zone'], "#FFD740"))
            if rec.get('stop_loss'):
                render_html(metric_row("Stop Loss", rec['stop_loss'], "#FF5252"))

        with col2:
            st.subheader("⚖️ Risk Profile")
            render_html(metric_row("Risk Level", rec['risk_level']))
            render_html(metric_row("Risk/Reward", rec['risk_reward']))

        with col3:
            st.subheader("🎯 Suitability")
            for style in rec['suitability']:
                render_html(signal_badge(style, "#00D4FF"))

        # ── Technical Signals Detail ─────────────────────────
        tech = result['technical']
        if tech.get('signals'):
            st.markdown("---")
            st.subheader("📈 Technical Indicator Signals")

            sig_data = []
            for name, info in tech['signals'].items():
                sig_data.append({
                    "Indicator": name,
                    "Value": str(info.get('value', 'N/A')),
                    "Signal": info.get('signal', 'N/A'),
                    "Score": info.get('score', 50),
                })
            if sig_data:
                df = pd.DataFrame(sig_data)
                st.dataframe(df, use_container_width=True, hide_index=True)

        # ── Fundamental Detail ───────────────────────────────
        fund = result['fundamental']
        if fund.get('metrics'):
            st.markdown("---")
            st.subheader("🏢 Fundamental Metrics")

            fund_data = []
            for name, info in fund['metrics'].items():
                fund_data.append({
                    "Metric": name,
                    "Value": str(info.get('value', 'N/A')),
                    "Assessment": info.get('assessment', 'N/A'),
                    "Score": info.get('score', 50),
                })
            if fund_data:
                df = pd.DataFrame(fund_data)
                st.dataframe(df, use_container_width=True, hide_index=True)

        # ── Risk Detail ──────────────────────────────────────
        risk = result['risk']
        if risk.get('metrics'):
            st.markdown("---")
            st.subheader("🛡️ Risk Metrics")

            col1, col2 = st.columns([1, 1])
            with col1:
                risk_data = []
                for name, info in risk['metrics'].items():
                    risk_data.append({
                        "Metric": name,
                        "Value": str(info.get('value', 'N/A')),
                        "Assessment": str(info.get('assessment', '')),
                    })
                if risk_data:
                    df = pd.DataFrame(risk_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
            with col2:
                fig = create_risk_gauge(risk['score'], 'Risk Score (higher = safer)')
                st.plotly_chart(fig, use_container_width=True)

        # ── Support / Resistance ─────────────────────────────
        sr = result.get('support_resistance')
        if sr:
            st.markdown("---")
            st.subheader("📐 Support & Resistance Levels")

            col1, col2 = st.columns(2)
            with col1:
                render_html(metric_row("Pivot", f"₹{sr.get('pivot', 0):,.2f}"))
                render_html(metric_row("Support 1", f"₹{sr.get('support_1', 0):,.2f}", "#00C853"))
                render_html(metric_row("Support 2", f"₹{sr.get('support_2', 0):,.2f}", "#00C853"))
                render_html(metric_row("Resistance 1", f"₹{sr.get('resistance_1', 0):,.2f}", "#FF5252"))
                render_html(metric_row("Resistance 2", f"₹{sr.get('resistance_2', 0):,.2f}", "#FF5252"))

            with col2:
                if sr.get('fibonacci'):
                    st.markdown("**Fibonacci Retracement:**")
                    for label, val in sr['fibonacci'].items():
                        render_html(metric_row(label, f"₹{val:,.2f}"))

        # ── Disclaimer ───────────────────────────────────────
        st.markdown("---")
        st.info("""
        **⚠️ Disclaimer:** This AI analysis is for educational and informational purposes only.
        It should not be considered as financial advice. Always consult a qualified financial
        advisor before making investment decisions. Past performance does not guarantee future results.
        """)


def _run_analysis(ticker: str, period: str):
    """Run the complete AI analysis pipeline."""

    with st.spinner("🔄 Running AI analysis engine... This may take a moment."):
        # 1) Fetch data
        fetcher = StockDataFetcher(ticker)
        if not fetcher.validate_ticker():
            st.error(config.ERROR_MESSAGES['invalid_ticker'])
            return

        stock_info = fetcher.get_stock_info()
        if not stock_info:
            st.error(config.ERROR_MESSAGES['no_data'])
            return

        period_map = {"1 Year": "1y", "2 Years": "2y", "5 Years": "5y"}
        hist_data = fetcher.get_historical_data(period=period_map.get(period, "1y"))
        if hist_data is None or hist_data.empty:
            st.error(config.ERROR_MESSAGES['no_data'])
            return

        current_price = stock_info['current_price']

        # 2) Technical analysis
        tech_result = compute_technical_score(hist_data, current_price)

        # 3) Fundamental analysis
        fund_result = compute_fundamental_score(stock_info)

        # 4) Risk analysis
        risk_result = compute_risk_score(hist_data)

        # 5) Sentiment analysis
        sentiment_result = None
        try:
            articles = get_cached_news(ticker, days_back=7)
            if articles:
                analyzer = SentimentAnalyzer()
                sentiment_result = analyzer.analyze_news_articles(articles)
        except Exception:
            pass

        # 6) AI prediction (quick)
        prediction_result = None
        try:
            predictor, metrics, future_predictions = create_prediction_pipeline(
                hist_data, model_type='random_forest'
            )
            if metrics and future_predictions is not None and not future_predictions.empty:
                pred_30 = future_predictions.iloc[-1]['Predicted_Close']
                pct_change = (pred_30 - current_price) / current_price * 100
                prediction_result = {
                    "predicted_change_pct": pct_change,
                    "confidence": max(0, metrics.get('test_r2', 0)),
                    "predicted_price_30d": pred_30,
                }
        except Exception:
            pass

        # 7) Support / Resistance
        sr = compute_support_resistance(hist_data)

        # 8) Generate recommendation
        rec = generate_recommendation(
            technical_result=tech_result,
            fundamental_result=fund_result,
            sentiment_result=sentiment_result,
            prediction_result=prediction_result,
            risk_result=risk_result,
            current_price=current_price,
            support_resistance=sr,
        )

        # Store result
        st.session_state.ai_result = {
            'ticker': ticker,
            'current_price': current_price,
            'stock_info': stock_info,
            'recommendation': rec,
            'technical': tech_result,
            'fundamental': fund_result,
            'risk': risk_result,
            'sentiment': sentiment_result,
            'prediction': prediction_result,
            'support_resistance': sr,
        }

