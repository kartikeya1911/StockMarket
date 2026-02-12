"""
Stock Price Prediction Module
Implements machine learning models for stock price prediction
"""

import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
import config

class StockPredictor:
    """
    Class to handle stock price prediction using machine learning
    """
    
    def __init__(self, data):
        """
        Initialize the Stock Predictor
        
        Args:
            data (pd.DataFrame): Historical stock data
        """
        self.data = data.copy()
        self.model = None
        self.scaler = MinMaxScaler()
        self.features = None
        self.target = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def prepare_data(self, target_column='Close', lookback_days=60):
        """
        Prepare data for machine learning
        
        Args:
            target_column (str): Column to predict
            lookback_days (int): Number of days to look back for features
        
        Returns:
            tuple: (X, y) features and target
        """
        try:
            # Sort by date
            df = self.data.sort_values('Date').reset_index(drop=True)
            
            # Create feature columns
            df['Days'] = range(len(df))
            
            # Add technical features
            df['MA_5'] = df[target_column].rolling(window=5).mean()
            df['MA_10'] = df[target_column].rolling(window=10).mean()
            df['MA_20'] = df[target_column].rolling(window=20).mean()
            df['Volatility'] = df[target_column].rolling(window=10).std()
            df['Daily_Return'] = df[target_column].pct_change()
            
            # Add day of week and month
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                df['Day_of_Week'] = df['Date'].dt.dayofweek
                df['Month'] = df['Date'].dt.month
            
            # Drop rows with NaN values
            df = df.dropna()
            
            # Select features
            feature_columns = [
                'Days', 'Open', 'High', 'Low', 'Volume',
                'MA_5', 'MA_10', 'MA_20', 'Volatility', 'Daily_Return'
            ]
            
            # Add day/month if available
            if 'Day_of_Week' in df.columns:
                feature_columns.extend(['Day_of_Week', 'Month'])
            
            self.features = df[feature_columns]
            self.target = df[target_column]
            
            return self.features, self.target
        
        except Exception as e:
            st.error(f"Error preparing data: {str(e)}")
            return None, None
    
    def split_data(self, test_size=0.2, random_state=42):
        """
        Split data into training and testing sets
        
        Args:
            test_size (float): Proportion of test data
            random_state (int): Random seed
        
        Returns:
            bool: True if successful
        """
        try:
            if self.features is None or self.target is None:
                st.error("Please prepare data first using prepare_data()")
                return False
            
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                self.features, self.target,
                test_size=test_size,
                random_state=random_state,
                shuffle=False  # Don't shuffle time series data
            )
            
            return True
        
        except Exception as e:
            st.error(f"Error splitting data: {str(e)}")
            return False
    
    def train_linear_regression(self):
        """
        Train a Linear Regression model
        
        Returns:
            dict: Model performance metrics
        """
        try:
            if self.X_train is None:
                st.error("Please split data first using split_data()")
                return None
            
            # Initialize and train model
            self.model = LinearRegression()
            self.model.fit(self.X_train, self.y_train)
            
            # Make predictions
            train_predictions = self.model.predict(self.X_train)
            test_predictions = self.model.predict(self.X_test)
            
            # Calculate metrics
            metrics = {
                'model_name': 'Linear Regression',
                'train_rmse': np.sqrt(mean_squared_error(self.y_train, train_predictions)),
                'test_rmse': np.sqrt(mean_squared_error(self.y_test, test_predictions)),
                'train_mae': mean_absolute_error(self.y_train, train_predictions),
                'test_mae': mean_absolute_error(self.y_test, test_predictions),
                'train_r2': r2_score(self.y_train, train_predictions),
                'test_r2': r2_score(self.y_test, test_predictions),
                'train_predictions': train_predictions,
                'test_predictions': test_predictions
            }
            
            return metrics
        
        except Exception as e:
            st.error(f"Error training model: {str(e)}")
            return None
    
    def train_random_forest(self, n_estimators=100, max_depth=10):
        """
        Train a Random Forest Regressor model
        
        Args:
            n_estimators (int): Number of trees
            max_depth (int): Maximum depth of trees
        
        Returns:
            dict: Model performance metrics
        """
        try:
            if self.X_train is None:
                st.error("Please split data first using split_data()")
                return None
            
            # Initialize and train model
            self.model = RandomForestRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=config.RANDOM_STATE,
                n_jobs=-1
            )
            self.model.fit(self.X_train, self.y_train)
            
            # Make predictions
            train_predictions = self.model.predict(self.X_train)
            test_predictions = self.model.predict(self.X_test)
            
            # Calculate metrics
            metrics = {
                'model_name': 'Random Forest',
                'train_rmse': np.sqrt(mean_squared_error(self.y_train, train_predictions)),
                'test_rmse': np.sqrt(mean_squared_error(self.y_test, test_predictions)),
                'train_mae': mean_absolute_error(self.y_train, train_predictions),
                'test_mae': mean_absolute_error(self.y_test, test_predictions),
                'train_r2': r2_score(self.y_train, train_predictions),
                'test_r2': r2_score(self.y_test, test_predictions),
                'train_predictions': train_predictions,
                'test_predictions': test_predictions,
                'feature_importance': self.model.feature_importances_
            }
            
            return metrics
        
        except Exception as e:
            st.error(f"Error training Random Forest: {str(e)}")
            return None
    
    def predict_future(self, days=30):
        """
        Predict future stock prices
        
        Args:
            days (int): Number of days to predict
        
        Returns:
            pd.DataFrame: Future predictions
        """
        try:
            if self.model is None:
                st.error("Please train a model first")
                return None
            
            # Get the last known values
            last_row = self.features.iloc[-1].copy()
            last_date = self.data['Date'].iloc[-1]
            last_close = self.data['Close'].iloc[-1]
            
            predictions = []
            dates = []
            
            # Make predictions for future days
            for i in range(1, days + 1):
                # Create feature vector for prediction
                future_features = last_row.copy()
                future_features['Days'] = last_row['Days'] + i
                
                # Predict
                predicted_price = self.model.predict([future_features.values])[0]
                
                # Store prediction
                predictions.append(predicted_price)
                future_date = last_date + timedelta(days=i)
                dates.append(future_date)
                
                # Update moving features for next prediction
                # (Simple approach - can be improved)
                last_row['MA_5'] = predicted_price
                last_row['MA_10'] = predicted_price
                last_row['MA_20'] = predicted_price
            
            # Create DataFrame with predictions
            future_df = pd.DataFrame({
                'Date': dates,
                'Predicted_Close': predictions
            })
            
            return future_df
        
        except Exception as e:
            st.error(f"Error predicting future prices: {str(e)}")
            return None
    
    def get_feature_importance(self):
        """
        Get feature importance (for tree-based models)
        
        Returns:
            pd.DataFrame: Feature importance
        """
        try:
            if self.model is None:
                return None
            
            if hasattr(self.model, 'feature_importances_'):
                importance_df = pd.DataFrame({
                    'Feature': self.features.columns,
                    'Importance': self.model.feature_importances_
                }).sort_values('Importance', ascending=False)
                
                return importance_df
            else:
                return None
        
        except Exception as e:
            return None


# ==================== HELPER FUNCTIONS ====================

def create_prediction_pipeline(data, model_type='linear'):
    """
    Complete prediction pipeline
    
    Args:
        data (pd.DataFrame): Historical stock data
        model_type (str): 'linear' or 'random_forest'
    
    Returns:
        tuple: (predictor, metrics, future_predictions)
    """
    try:
        # Initialize predictor
        predictor = StockPredictor(data)
        
        # Prepare data
        X, y = predictor.prepare_data()
        if X is None or y is None:
            return None, None, None
        
        # Split data
        if not predictor.split_data(test_size=0.2):
            return None, None, None
        
        # Train model
        if model_type == 'linear':
            metrics = predictor.train_linear_regression()
        else:
            metrics = predictor.train_random_forest()
        
        if metrics is None:
            return None, None, None
        
        # Predict future
        future_predictions = predictor.predict_future(days=config.PREDICTION_DAYS)
        
        return predictor, metrics, future_predictions
    
    except Exception as e:
        st.error(f"Error in prediction pipeline: {str(e)}")
        return None, None, None


def calculate_prediction_confidence(metrics):
    """
    Calculate confidence level based on model metrics
    
    Args:
        metrics (dict): Model performance metrics
    
    Returns:
        dict: Confidence information
    """
    try:
        r2_score = metrics.get('test_r2', 0)
        
        # Determine confidence level based on R² score
        if r2_score >= 0.8:
            confidence = "High"
            color = "green"
            message = "Model shows strong predictive capability"
        elif r2_score >= 0.6:
            confidence = "Moderate"
            color = "orange"
            message = "Model shows reasonable predictive capability"
        elif r2_score >= 0.4:
            confidence = "Low"
            color = "red"
            message = "Model has limited predictive capability"
        else:
            confidence = "Very Low"
            color = "darkred"
            message = "Model predictions may not be reliable"
        
        return {
            'confidence': confidence,
            'color': color,
            'message': message,
            'r2_score': r2_score
        }
    
    except Exception as e:
        return {
            'confidence': "Unknown",
            'color': "gray",
            'message': "Unable to determine confidence",
            'r2_score': 0
        }


def format_prediction_summary(metrics, future_predictions, current_price):
    """
    Create a formatted summary of predictions
    
    Args:
        metrics (dict): Model metrics
        future_predictions (pd.DataFrame): Future price predictions
        current_price (float): Current stock price
    
    Returns:
        dict: Prediction summary
    """
    try:
        if future_predictions is None or future_predictions.empty:
            return None
        
        # Get predictions for different timeframes
        pred_7_days = future_predictions.iloc[6]['Predicted_Close'] if len(future_predictions) >= 7 else None
        pred_30_days = future_predictions.iloc[-1]['Predicted_Close']
        
        # Calculate expected changes
        change_7_days = ((pred_7_days - current_price) / current_price * 100) if pred_7_days else None
        change_30_days = (pred_30_days - current_price) / current_price * 100
        
        summary = {
            'current_price': current_price,
            'predicted_7_days': pred_7_days,
            'predicted_30_days': pred_30_days,
            'change_7_days': change_7_days,
            'change_30_days': change_30_days,
            'model_accuracy': metrics.get('test_r2', 0),
            'model_name': metrics.get('model_name', 'Unknown')
        }
        
        return summary
    
    except Exception as e:
        return None


def simple_moving_average_prediction(data, window=20, periods=30):
    """
    Simple prediction based on moving average trend
    (Alternative lightweight prediction method)
    
    Args:
        data (pd.DataFrame): Historical stock data
        window (int): Moving average window
        periods (int): Number of periods to predict
    
    Returns:
        pd.DataFrame: Predictions
    """
    try:
        # Calculate moving average
        ma = data['Close'].rolling(window=window).mean()
        
        # Calculate trend
        recent_ma = ma.tail(window)
        trend = (recent_ma.iloc[-1] - recent_ma.iloc[0]) / len(recent_ma)
        
        # Generate predictions
        last_price = data['Close'].iloc[-1]
        last_date = data['Date'].iloc[-1]
        
        predictions = []
        dates = []
        
        for i in range(1, periods + 1):
            predicted_price = last_price + (trend * i)
            predictions.append(predicted_price)
            dates.append(last_date + timedelta(days=i))
        
        return pd.DataFrame({
            'Date': dates,
            'Predicted_Close': predictions
        })
    
    except Exception as e:
        return None
