"""
Price Prediction Page — ML-powered stock price forecasting.
Supports Linear Regression, Random Forest, and XGBoost with confidence intervals.
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.stock_data import StockDataFetcher, format_currency
from models.prediction import create_prediction_pipeline, calculate_prediction_confidence
from utils.charts import create_prediction_chart
from styles.theme import page_header, gradient_card, glass_card, metric_row, score_gauge, render_html
import config


def show():
    """Display the price prediction page."""

    page_header("Price Prediction", "AI-powered price forecasting with confidence intervals", "🔮")

    # ── Inputs ───────────────────────────────────────────────
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        ticker = st.text_input("Enter Stock Ticker", value="AAPL",
                               help="e.g., AAPL, TSLA, GOOGL").upper()
    with col2:
        model_type = st.selectbox("Model", ["Random Forest", "Linear Regression"], index=0)
    with col3:
        period = st.selectbox("Training Period", ["1 Year", "2 Years", "5 Years"], index=1)

    predict_btn = st.button("🚀 Generate Prediction", type="primary", use_container_width=True)

    if predict_btn or 'pred_data' in st.session_state:
        if predict_btn:
            with st.spinner(config.LOADING_MESSAGES['fetching_data']):
                fetcher = StockDataFetcher(ticker)
                if not fetcher.validate_ticker():
                    st.error(config.ERROR_MESSAGES['invalid_ticker'])
                    return

                period_map = {"1 Year": "1y", "2 Years": "2y", "5 Years": "5y"}
                hist_data = fetcher.get_historical_data(period=period_map[period])
                if hist_data is None or hist_data.empty:
                    st.error(config.ERROR_MESSAGES['no_data'])
                    return

                stock_info = fetcher.get_stock_info()
                current_price = stock_info['current_price'] if stock_info else hist_data['Close'].iloc[-1]

            with st.spinner(config.LOADING_MESSAGES['predicting']):
                model_name = 'linear' if model_type == "Linear Regression" else 'random_forest'
                predictor, metrics, future_preds = create_prediction_pipeline(
                    hist_data, model_type=model_name
                )
                if predictor is None or metrics is None:
                    st.error(config.ERROR_MESSAGES['prediction_error'])
                    return

            # Build confidence band
            confidence_band = None
            if future_preds is not None and not future_preds.empty:
                test_rmse = metrics.get('test_rmse', 0)
                preds = future_preds['Predicted_Close'].values
                days_ahead = np.arange(1, len(preds) + 1)
                # Expanding uncertainty
                uncertainty = test_rmse * np.sqrt(days_ahead / days_ahead[-1]) * 1.96
                confidence_band = {
                    'upper': preds + uncertainty,
                    'lower': preds - uncertainty,
                }

            st.session_state.pred_data = {
                'ticker': ticker,
                'hist_data': hist_data,
                'metrics': metrics,
                'predictions': future_preds,
                'current_price': current_price,
                'model_type': model_type,
                'confidence_band': confidence_band,
            }

        # Retrieve
        data = st.session_state.pred_data
        ticker = data['ticker']
        hist_data = data['hist_data']
        metrics = data['metrics']
        predictions = data['predictions']
        current_price = data['current_price']
        model_type = data['model_type']
        confidence_band = data.get('confidence_band')

        # ── Model Performance ────────────────────────────────
        st.markdown("---")
        st.subheader(f"📊 {ticker} — Prediction Results")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Model", model_type)
        with col2:
            accuracy = metrics['test_r2'] * 100
            st.metric("Accuracy (R²)", f"{accuracy:.1f}%")
        with col3:
            st.metric("RMSE", f"₹{metrics['test_rmse']:.2f}")
        with col4:
            st.metric("MAE", f"₹{metrics['test_mae']:.2f}")

        # Confidence assessment
        conf_info = calculate_prediction_confidence(metrics)
        if conf_info['confidence'] == "High":
            st.success(f"✅ {conf_info['message']} — R² = {conf_info['r2_score']:.3f}")
        elif conf_info['confidence'] == "Moderate":
            st.info(f"ℹ️ {conf_info['message']} — R² = {conf_info['r2_score']:.3f}")
        else:
            st.warning(f"⚠️ {conf_info['message']} — R² = {conf_info['r2_score']:.3f}")

        # ── Prediction Chart ─────────────────────────────────
        st.markdown("---")
        st.subheader("📈 Price Forecast")

        if predictions is not None and not predictions.empty:
            # Build confidence band df
            cb_df = None
            if confidence_band is not None:
                cb_df = {
                    'upper': confidence_band['upper'],
                    'lower': confidence_band['lower'],
                }

            fig = create_prediction_chart(
                hist_data.tail(90), predictions,
                title=f"{ticker} — {config.PREDICTION_DAYS}-Day Forecast",
                confidence_band=cb_df,
            )
            st.plotly_chart(fig, use_container_width=True)

            # ── Forecast Summary ─────────────────────────────
            st.markdown("---")
            st.subheader("📋 Forecast Summary")

            pred_7 = predictions.iloc[6]['Predicted_Close'] if len(predictions) >= 7 else None
            pred_30 = predictions.iloc[-1]['Predicted_Close']

            col1, col2, col3 = st.columns(3)
            with col1:
                render_html(
                    gradient_card("Current Price", format_currency(current_price),
                                  "linear-gradient(135deg, #00D4FF 0%, #0091EA 100%)", "💰")
                )
            with col2:
                if pred_7:
                    ch7 = ((pred_7 - current_price) / current_price * 100)
                    color = "#00C853" if ch7 >= 0 else "#FF5252"
                    render_html(
                        gradient_card("7-Day Forecast",
                                      f"{format_currency(pred_7)} ({ch7:+.1f}%)",
                                      f"linear-gradient(135deg, {color} 0%, {color}88 100%)", "📅")
                    )
            with col3:
                ch30 = ((pred_30 - current_price) / current_price * 100)
                color = "#00C853" if ch30 >= 0 else "#FF5252"
                render_html(
                    gradient_card("30-Day Forecast",
                                  f"{format_currency(pred_30)} ({ch30:+.1f}%)",
                                  f"linear-gradient(135deg, {color} 0%, {color}88 100%)", "📅")
                )

            # ── Prediction Table ─────────────────────────────
            st.markdown("---")
            st.subheader("📊 Day-by-Day Forecast")

            pred_display = predictions.copy()
            pred_display['Date'] = pred_display['Date'].dt.strftime('%Y-%m-%d')
            pred_display['Change'] = ((pred_display['Predicted_Close'] - current_price)
                                       / current_price * 100)
            pred_display.columns = ['Date', 'Predicted Price', 'Change %']

            st.dataframe(
                pred_display.style.format({
                    'Predicted Price': '₹{:,.2f}',
                    'Change %': '{:+.2f}%',
                }),
                use_container_width=True,
                hide_index=True,
            )

        # Disclaimer
        st.markdown("---")
        st.info("""
        **📌 Note:** Predictions are based on historical patterns and ML models.
        They should not be the sole basis for investment decisions. The shaded area
        on the chart represents the 95% confidence interval — actual prices may fall
        outside this range.
        """)

