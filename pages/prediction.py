"""
Price Prediction Page
Machine learning-based stock price prediction
"""

import streamlit as st
from utils.stock_data import StockDataFetcher, format_currency
from models.prediction import create_prediction_pipeline, calculate_prediction_confidence
from utils.charts import create_prediction_chart
import config

def show():
    """Display price prediction page"""
    
    st.markdown("""
        <h1 style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🔮 Stock Price Prediction</h1>
        <p style='font-size: 1.1rem; color: #6b7280;'>AI-powered price predictions using machine learning</p>
    """, unsafe_allow_html=True)
    
    # Input section
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        ticker = st.text_input(
            "Enter Stock Ticker",
            value="AAPL",
            help="e.g., AAPL, TSLA, GOOGL"
        ).upper()
    
    with col2:
        model_type = st.selectbox(
            "Model Type",
            ["Linear Regression", "Random Forest"],
            index=0
        )
    
    with col3:
        period = st.selectbox(
            "Training Period",
            ["1 Year", "2 Years", "5 Years"],
            index=1
        )
    
    predict_button = st.button("🚀 Generate Prediction", type="primary")
    
    if predict_button or 'prediction_data' in st.session_state:
        if predict_button:
            # Fetch data
            with st.spinner(config.LOADING_MESSAGES['fetching_data']):
                fetcher = StockDataFetcher(ticker)
                
                if not fetcher.validate_ticker():
                    st.error(config.ERROR_MESSAGES['invalid_ticker'])
                    return
                
                # Map period to yfinance format
                period_map = {"1 Year": "1y", "2 Years": "2y", "5 Years": "5y"}
                hist_data = fetcher.get_historical_data(period=period_map[period])
                
                if hist_data is None or hist_data.empty:
                    st.error(config.ERROR_MESSAGES['no_data'])
                    return
                
                stock_info = fetcher.get_stock_info()
                current_price = stock_info['current_price'] if stock_info else hist_data['Close'].iloc[-1]
            
            # Train model and predict
            with st.spinner(config.LOADING_MESSAGES['predicting']):
                model_name = 'linear' if model_type == "Linear Regression" else 'random_forest'
                predictor, metrics, future_predictions = create_prediction_pipeline(
                    hist_data,
                    model_type=model_name
                )
                
                if predictor is None or metrics is None:
                    st.error(config.ERROR_MESSAGES['prediction_error'])
                    return
            
            # Store in session state
            st.session_state.prediction_data = {
                'ticker': ticker,
                'hist_data': hist_data,
                'metrics': metrics,
                'predictions': future_predictions,
                'current_price': current_price,
                'model_type': model_type
            }
        
        # Retrieve from session state
        data = st.session_state.prediction_data
        ticker = data['ticker']
        hist_data = data['hist_data']
        metrics = data['metrics']
        predictions = data['predictions']
        current_price = data['current_price']
        model_type = data['model_type']
        
        st.success(config.SUCCESS_MESSAGES['prediction_complete'])
        
        # Display predictions
        st.markdown("---")
        st.header(f"📊 Prediction Results for {ticker}")
        
        # Model performance metrics
        st.subheader("🎯 Model Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Model Type",
                model_type
            )
        
        with col2:
            accuracy = metrics['test_r2'] * 100
            st.metric(
                "Accuracy (R²)",
                f"{accuracy:.2f}%"
            )
        
        with col3:
            st.metric(
                "Test RMSE",
                f"₹{metrics['test_rmse']:.2f}"
            )
        
        with col4:
            st.metric(
                "Test MAE",
                f"₹{metrics['test_mae']:.2f}"
            )
        
        # Confidence level
        confidence_info = calculate_prediction_confidence(metrics)
        
        if confidence_info['confidence'] == "High":
            st.success(f"✅ {confidence_info['message']}")
        elif confidence_info['confidence'] == "Moderate":
            st.info(f"ℹ️ {confidence_info['message']}")
        else:
            st.warning(f"⚠️ {confidence_info['message']}")
        
        # Prediction chart
        st.markdown("---")
        st.subheader("📈 Price Prediction Chart")
        
        if predictions is not None and not predictions.empty:
            fig = create_prediction_chart(
                hist_data.tail(90),  # Last 90 days
                predictions,
                title=f"{ticker} Price Prediction - Next {config.PREDICTION_DAYS} Days"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Prediction summary
            st.markdown("---")
            st.subheader("📋 Prediction Summary")
            
            col1, col2, col3 = st.columns(3)
            
            pred_7_days = predictions.iloc[6]['Predicted_Close'] if len(predictions) >= 7 else None
            pred_30_days = predictions.iloc[-1]['Predicted_Close']
            
            with col1:
                st.metric(
                    "Current Price",
                    format_currency(current_price)
                )
            
            with col2:
                if pred_7_days:
                    change_7 = ((pred_7_days - current_price) / current_price * 100)
                    st.metric(
                        "7-Day Prediction",
                        format_currency(pred_7_days),
                        f"{change_7:+.2f}%"
                    )
            
            with col3:
                change_30 = ((pred_30_days - current_price) / current_price * 100)
                st.metric(
                    "30-Day Prediction",
                    format_currency(pred_30_days),
                    f"{change_30:+.2f}%"
                )
            
            # Prediction table
            st.markdown("---")
            st.subheader("📊 Detailed Predictions")
            
            pred_display = predictions.copy()
            pred_display['Date'] = pred_display['Date'].dt.strftime('%Y-%m-%d')
            pred_display['Predicted_Close'] = pred_display['Predicted_Close'].apply(
                lambda x: f"₹{x:.2f}"
            )
            pred_display.columns = ['Date', 'Predicted Price']
            
            st.dataframe(pred_display, use_container_width=True, hide_index=True)
        
        # Important note
        st.markdown("---")
        st.info("""
        **📌 Note:** Predictions are based on historical data and machine learning models.
        They should be used as one of many tools for analysis, not as the sole basis for
        investment decisions. Market conditions can change rapidly due to various factors.
        """)
