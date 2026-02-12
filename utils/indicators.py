"""
Technical Indicators Module
Calculates various technical indicators for stock analysis
"""

import pandas as pd
import numpy as np
import streamlit as st
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator, EMAIndicator
from ta.volatility import BollingerBands
import config

class TechnicalIndicators:
    """
    Class to calculate technical indicators for stock data
    """
    
    def __init__(self, data):
        """
        Initialize Technical Indicators calculator
        
        Args:
            data (pd.DataFrame): Historical stock data with OHLCV columns
        """
        self.data = data.copy()
        
        # Ensure we have the required columns
        required_columns = ['Close', 'High', 'Low', 'Open', 'Volume']
        if not all(col in self.data.columns for col in required_columns):
            st.error("Data must contain Open, High, Low, Close, Volume columns")
            self.data = None
    
    def calculate_sma(self, window=20, column='Close'):
        """
        Calculate Simple Moving Average
        
        Args:
            window (int): Period for SMA calculation
            column (str): Column to calculate SMA on
        
        Returns:
            pd.Series: SMA values
        """
        try:
            indicator = SMAIndicator(close=self.data[column], window=window)
            return indicator.sma_indicator()
        except Exception as e:
            st.error(f"Error calculating SMA: {str(e)}")
            return None
    
    def calculate_ema(self, window=20, column='Close'):
        """
        Calculate Exponential Moving Average
        
        Args:
            window (int): Period for EMA calculation
            column (str): Column to calculate EMA on
        
        Returns:
            pd.Series: EMA values
        """
        try:
            indicator = EMAIndicator(close=self.data[column], window=window)
            return indicator.ema_indicator()
        except Exception as e:
            st.error(f"Error calculating EMA: {str(e)}")
            return None
    
    def calculate_rsi(self, window=14):
        """
        Calculate Relative Strength Index (RSI)
        
        Args:
            window (int): Period for RSI calculation (default 14)
        
        Returns:
            pd.Series: RSI values
        """
        try:
            indicator = RSIIndicator(close=self.data['Close'], window=window)
            rsi = indicator.rsi()
            return rsi
        except Exception as e:
            st.error(f"Error calculating RSI: {str(e)}")
            return None
    
    def calculate_macd(self, fast=12, slow=26, signal=9):
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            fast (int): Fast period (default 12)
            slow (int): Slow period (default 26)
            signal (int): Signal period (default 9)
        
        Returns:
            dict: Dictionary containing MACD line, signal line, and histogram
        """
        try:
            indicator = MACD(
                close=self.data['Close'],
                window_fast=fast,
                window_slow=slow,
                window_sign=signal
            )
            
            macd_data = {
                'macd': indicator.macd(),
                'signal': indicator.macd_signal(),
                'histogram': indicator.macd_diff()
            }
            
            return macd_data
        except Exception as e:
            st.error(f"Error calculating MACD: {str(e)}")
            return None
    
    def calculate_bollinger_bands(self, window=20, std_dev=2):
        """
        Calculate Bollinger Bands
        
        Args:
            window (int): Period for Bollinger Bands (default 20)
            std_dev (float): Standard deviation multiplier (default 2)
        
        Returns:
            dict: Dictionary containing upper, middle, and lower bands
        """
        try:
            indicator = BollingerBands(
                close=self.data['Close'],
                window=window,
                window_dev=std_dev
            )
            
            bb_data = {
                'upper': indicator.bollinger_hband(),
                'middle': indicator.bollinger_mavg(),
                'lower': indicator.bollinger_lband(),
                'bandwidth': indicator.bollinger_wband(),
                'pband': indicator.bollinger_pband()
            }
            
            return bb_data
        except Exception as e:
            st.error(f"Error calculating Bollinger Bands: {str(e)}")
            return None
    
    def calculate_all_indicators(self):
        """
        Calculate all major technical indicators
        
        Returns:
            pd.DataFrame: DataFrame with all indicators added
        """
        try:
            result_df = self.data.copy()
            
            # Moving Averages
            result_df['SMA_50'] = self.calculate_sma(window=config.MA_SHORT_PERIOD)
            result_df['SMA_200'] = self.calculate_sma(window=config.MA_LONG_PERIOD)
            result_df['EMA_20'] = self.calculate_ema(window=20)
            
            # RSI
            result_df['RSI'] = self.calculate_rsi(window=config.RSI_PERIOD)
            
            # MACD
            macd_data = self.calculate_macd(
                fast=config.MACD_FAST,
                slow=config.MACD_SLOW,
                signal=config.MACD_SIGNAL
            )
            if macd_data:
                result_df['MACD'] = macd_data['macd']
                result_df['MACD_Signal'] = macd_data['signal']
                result_df['MACD_Histogram'] = macd_data['histogram']
            
            # Bollinger Bands
            bb_data = self.calculate_bollinger_bands(
                window=config.BB_PERIOD,
                std_dev=config.BB_STD_DEV
            )
            if bb_data:
                result_df['BB_Upper'] = bb_data['upper']
                result_df['BB_Middle'] = bb_data['middle']
                result_df['BB_Lower'] = bb_data['lower']
            
            return result_df
        
        except Exception as e:
            st.error(f"Error calculating indicators: {str(e)}")
            return self.data
    
    def get_rsi_signal(self, rsi_value):
        """
        Get trading signal based on RSI value
        
        Args:
            rsi_value (float): Current RSI value
        
        Returns:
            dict: Signal information
        """
        if rsi_value is None or pd.isna(rsi_value):
            return {"signal": "Neutral", "message": "Insufficient data"}
        
        if rsi_value >= config.RSI_OVERBOUGHT:
            return {
                "signal": "Overbought",
                "message": f"RSI at {rsi_value:.2f} indicates overbought conditions. Consider selling.",
                "color": "red"
            }
        elif rsi_value <= config.RSI_OVERSOLD:
            return {
                "signal": "Oversold",
                "message": f"RSI at {rsi_value:.2f} indicates oversold conditions. Consider buying.",
                "color": "green"
            }
        else:
            return {
                "signal": "Neutral",
                "message": f"RSI at {rsi_value:.2f} indicates neutral market conditions.",
                "color": "gray"
            }
    
    def get_macd_signal(self, macd_data):
        """
        Get trading signal based on MACD
        
        Args:
            macd_data (dict): Dictionary with MACD values
        
        Returns:
            dict: Signal information
        """
        if not macd_data or macd_data['macd'] is None:
            return {"signal": "Neutral", "message": "Insufficient data"}
        
        try:
            # Get the latest values
            macd_line = macd_data['macd'].iloc[-1]
            signal_line = macd_data['signal'].iloc[-1]
            histogram = macd_data['histogram'].iloc[-1]
            
            # Check for crossovers (if we have enough data)
            if len(macd_data['macd']) > 1:
                prev_histogram = macd_data['histogram'].iloc[-2]
                
                # Bullish crossover
                if prev_histogram < 0 and histogram > 0:
                    return {
                        "signal": "Bullish Crossover",
                        "message": "MACD crossed above signal line. Buy signal.",
                        "color": "green"
                    }
                # Bearish crossover
                elif prev_histogram > 0 and histogram < 0:
                    return {
                        "signal": "Bearish Crossover",
                        "message": "MACD crossed below signal line. Sell signal.",
                        "color": "red"
                    }
            
            # General position
            if macd_line > signal_line:
                return {
                    "signal": "Bullish",
                    "message": "MACD is above signal line. Bullish trend.",
                    "color": "green"
                }
            else:
                return {
                    "signal": "Bearish",
                    "message": "MACD is below signal line. Bearish trend.",
                    "color": "red"
                }
        
        except Exception as e:
            return {"signal": "Neutral", "message": "Error analyzing MACD"}
    
    def get_bollinger_signal(self, bb_data, current_price):
        """
        Get trading signal based on Bollinger Bands
        
        Args:
            bb_data (dict): Bollinger Bands data
            current_price (float): Current stock price
        
        Returns:
            dict: Signal information
        """
        if not bb_data or bb_data['upper'] is None:
            return {"signal": "Neutral", "message": "Insufficient data"}
        
        try:
            upper_band = bb_data['upper'].iloc[-1]
            lower_band = bb_data['lower'].iloc[-1]
            middle_band = bb_data['middle'].iloc[-1]
            
            # Calculate position within bands
            if current_price >= upper_band:
                return {
                    "signal": "Overbought",
                    "message": "Price is at or above upper Bollinger Band. Potential reversal.",
                    "color": "red"
                }
            elif current_price <= lower_band:
                return {
                    "signal": "Oversold",
                    "message": "Price is at or below lower Bollinger Band. Potential bounce.",
                    "color": "green"
                }
            elif current_price > middle_band:
                return {
                    "signal": "Above Average",
                    "message": "Price is above the middle band. Moderate bullish.",
                    "color": "lightgreen"
                }
            else:
                return {
                    "signal": "Below Average",
                    "message": "Price is below the middle band. Moderate bearish.",
                    "color": "orange"
                }
        
        except Exception as e:
            return {"signal": "Neutral", "message": "Error analyzing Bollinger Bands"}
    
    def get_moving_average_signal(self, sma_50, sma_200):
        """
        Get trading signal based on moving average crossover (Golden Cross / Death Cross)
        
        Args:
            sma_50 (pd.Series): 50-day SMA
            sma_200 (pd.Series): 200-day SMA
        
        Returns:
            dict: Signal information
        """
        if sma_50 is None or sma_200 is None:
            return {"signal": "Neutral", "message": "Insufficient data"}
        
        try:
            # Get current values
            current_sma_50 = sma_50.iloc[-1]
            current_sma_200 = sma_200.iloc[-1]
            
            # Check for crossover if we have enough data
            if len(sma_50) > 1 and len(sma_200) > 1:
                prev_sma_50 = sma_50.iloc[-2]
                prev_sma_200 = sma_200.iloc[-2]
                
                # Golden Cross - bullish signal
                if prev_sma_50 < prev_sma_200 and current_sma_50 > current_sma_200:
                    return {
                        "signal": "Golden Cross",
                        "message": "50-day MA crossed above 200-day MA. Strong buy signal!",
                        "color": "green"
                    }
                # Death Cross - bearish signal
                elif prev_sma_50 > prev_sma_200 and current_sma_50 < current_sma_200:
                    return {
                        "signal": "Death Cross",
                        "message": "50-day MA crossed below 200-day MA. Strong sell signal!",
                        "color": "red"
                    }
            
            # General position
            if current_sma_50 > current_sma_200:
                return {
                    "signal": "Bullish Trend",
                    "message": "50-day MA is above 200-day MA. Long-term bullish trend.",
                    "color": "green"
                }
            else:
                return {
                    "signal": "Bearish Trend",
                    "message": "50-day MA is below 200-day MA. Long-term bearish trend.",
                    "color": "red"
                }
        
        except Exception as e:
            return {"signal": "Neutral", "message": "Error analyzing moving averages"}


# ==================== HELPER FUNCTIONS ====================

def calculate_support_resistance(data, window=20):
    """
    Calculate support and resistance levels
    
    Args:
        data (pd.DataFrame): Historical stock data
        window (int): Lookback window
    
    Returns:
        dict: Support and resistance levels
    """
    try:
        # Recent high and low
        recent_high = data['High'].tail(window).max()
        recent_low = data['Low'].tail(window).min()
        
        # Overall high and low
        all_time_high = data['High'].max()
        all_time_low = data['Low'].min()
        
        return {
            'resistance': recent_high,
            'support': recent_low,
            'all_time_high': all_time_high,
            'all_time_low': all_time_low
        }
    except Exception as e:
        return None


def calculate_atr(data, period=14):
    """
    Calculate Average True Range (ATR) - measure of volatility
    
    Args:
        data (pd.DataFrame): Historical stock data
        period (int): ATR period
    
    Returns:
        pd.Series: ATR values
    """
    try:
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        
        atr = true_range.rolling(window=period).mean()
        return atr
    except Exception as e:
        return None


def calculate_obv(data):
    """
    Calculate On-Balance Volume (OBV)
    
    Args:
        data (pd.DataFrame): Historical stock data
    
    Returns:
        pd.Series: OBV values
    """
    try:
        obv = [0]
        for i in range(1, len(data)):
            if data['Close'].iloc[i] > data['Close'].iloc[i-1]:
                obv.append(obv[-1] + data['Volume'].iloc[i])
            elif data['Close'].iloc[i] < data['Close'].iloc[i-1]:
                obv.append(obv[-1] - data['Volume'].iloc[i])
            else:
                obv.append(obv[-1])
        
        return pd.Series(obv, index=data.index)
    except Exception as e:
        return None
