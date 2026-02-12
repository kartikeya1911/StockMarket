"""
Stock Data Fetching and Management Module
Handles all operations related to fetching and processing stock data using yfinance
"""

import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import config

class StockDataFetcher:
    """
    Class to handle stock data fetching and processing operations
    """
    
    def __init__(self, ticker):
        """
        Initialize the StockDataFetcher
        
        Args:
            ticker (str): Stock ticker symbol (e.g., 'AAPL', 'RELIANCE.NS')
        """
        self.ticker = ticker.upper()
        self.stock = None
        self.info = None
        
    def validate_ticker(self):
        """
        Validate if the ticker symbol is valid
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            self.stock = yf.Ticker(self.ticker)
            self.info = self.stock.info
            
            # Check if we got valid data
            if not self.info or 'regularMarketPrice' not in self.info:
                # Try alternative check
                hist = self.stock.history(period="5d")
                if hist.empty:
                    return False
            return True
        except Exception as e:
            st.error(f"Error validating ticker: {str(e)}")
            return False
    
    def get_stock_info(self):
        """
        Get comprehensive stock information
        
        Returns:
            dict: Dictionary containing stock information
        """
        try:
            if self.stock is None:
                self.stock = yf.Ticker(self.ticker)
                self.info = self.stock.info
            
            # Extract key information with fallbacks
            stock_info = {
                'symbol': self.ticker,
                'name': self.info.get('longName', self.ticker),
                'current_price': self.info.get('regularMarketPrice', 
                                               self.info.get('currentPrice', 0)),
                'previous_close': self.info.get('previousClose', 0),
                'open': self.info.get('regularMarketOpen', 
                                     self.info.get('open', 0)),
                'day_high': self.info.get('dayHigh', 0),
                'day_low': self.info.get('dayLow', 0),
                'volume': self.info.get('volume', 0),
                'market_cap': self.info.get('marketCap', 0),
                '52_week_high': self.info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': self.info.get('fiftyTwoWeekLow', 0),
                'pe_ratio': self.info.get('trailingPE', 0),
                'dividend_yield': self.info.get('dividendYield', 0),
                'beta': self.info.get('beta', 0),
                'sector': self.info.get('sector', 'N/A'),
                'industry': self.info.get('industry', 'N/A'),
                'website': self.info.get('website', 'N/A'),
                'description': self.info.get('longBusinessSummary', 'N/A')
            }
            
            return stock_info
        
        except Exception as e:
            st.error(f"Error fetching stock info: {str(e)}")
            return None
    
    def get_historical_data(self, period="1y", interval="1d"):
        """
        Fetch historical stock data
        
        Args:
            period (str): Time period (e.g., '1y', '6mo', '1d')
            interval (str): Data interval (e.g., '1d', '1wk', '1mo')
        
        Returns:
            pd.DataFrame: Historical stock data
        """
        try:
            if self.stock is None:
                self.stock = yf.Ticker(self.ticker)
            
            # Fetch historical data
            hist_data = self.stock.history(period=period, interval=interval)
            
            if hist_data.empty:
                st.warning(f"No historical data available for {self.ticker}")
                return None
            
            # Reset index to make Date a column
            hist_data.reset_index(inplace=True)
            
            return hist_data
        
        except Exception as e:
            st.error(f"Error fetching historical data: {str(e)}")
            return None
    
    def get_data_by_date_range(self, start_date, end_date, interval="1d"):
        """
        Fetch historical data for a specific date range
        
        Args:
            start_date (datetime): Start date
            end_date (datetime): End date
            interval (str): Data interval
        
        Returns:
            pd.DataFrame: Historical stock data
        """
        try:
            if self.stock is None:
                self.stock = yf.Ticker(self.ticker)
            
            hist_data = self.stock.history(start=start_date, end=end_date, 
                                          interval=interval)
            
            if hist_data.empty:
                return None
            
            hist_data.reset_index(inplace=True)
            return hist_data
        
        except Exception as e:
            st.error(f"Error fetching data by date range: {str(e)}")
            return None
    
    def get_realtime_price(self):
        """
        Get real-time stock price
        
        Returns:
            dict: Dictionary with current price and change information
        """
        try:
            if self.stock is None:
                self.stock = yf.Ticker(self.ticker)
                self.info = self.stock.info
            
            current_price = self.info.get('regularMarketPrice', 
                                         self.info.get('currentPrice', 0))
            previous_close = self.info.get('previousClose', 0)
            
            # Calculate change
            price_change = current_price - previous_close
            percent_change = (price_change / previous_close * 100) if previous_close else 0
            
            return {
                'current_price': current_price,
                'previous_close': previous_close,
                'price_change': price_change,
                'percent_change': percent_change
            }
        
        except Exception as e:
            st.error(f"Error fetching real-time price: {str(e)}")
            return None
    
    def get_dividends(self):
        """
        Get dividend history
        
        Returns:
            pd.DataFrame: Dividend history
        """
        try:
            if self.stock is None:
                self.stock = yf.Ticker(self.ticker)
            
            dividends = self.stock.dividends
            
            if dividends.empty:
                return None
            
            return dividends
        
        except Exception as e:
            st.error(f"Error fetching dividends: {str(e)}")
            return None
    
    def get_splits(self):
        """
        Get stock split history
        
        Returns:
            pd.DataFrame: Stock split history
        """
        try:
            if self.stock is None:
                self.stock = yf.Ticker(self.ticker)
            
            splits = self.stock.splits
            
            if splits.empty:
                return None
            
            return splits
        
        except Exception as e:
            st.error(f"Error fetching splits: {str(e)}")
            return None
    
    def get_major_holders(self):
        """
        Get major holders information
        
        Returns:
            pd.DataFrame: Major holders data
        """
        try:
            if self.stock is None:
                self.stock = yf.Ticker(self.ticker)
            
            holders = self.stock.major_holders
            return holders
        
        except Exception as e:
            return None
    
    def get_institutional_holders(self):
        """
        Get institutional holders
        
        Returns:
            pd.DataFrame: Institutional holders data
        """
        try:
            if self.stock is None:
                self.stock = yf.Ticker(self.ticker)
            
            inst_holders = self.stock.institutional_holders
            return inst_holders
        
        except Exception as e:
            return None


# ==================== HELPER FUNCTIONS ====================

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_stock_data(ticker, period="1y", interval="1d"):
    """
    Cached function to fetch stock data
    
    Args:
        ticker (str): Stock ticker symbol
        period (str): Time period
        interval (str): Data interval
    
    Returns:
        pd.DataFrame: Historical stock data
    """
    fetcher = StockDataFetcher(ticker)
    return fetcher.get_historical_data(period, interval)


@st.cache_data(ttl=60)  # Cache for 1 minute
def fetch_stock_info(ticker):
    """
    Cached function to fetch stock information
    
    Args:
        ticker (str): Stock ticker symbol
    
    Returns:
        dict: Stock information
    """
    fetcher = StockDataFetcher(ticker)
    if fetcher.validate_ticker():
        return fetcher.get_stock_info()
    return None


def format_large_number(num):
    """
    Format large numbers into readable format (K, M, B, T)
    
    Args:
        num (float): Number to format
    
    Returns:
        str: Formatted number string
    """
    if num == 0:
        return "0"
    
    try:
        num = float(num)
        if abs(num) >= 1e12:
            return f"{num/1e12:.2f}T"
        elif abs(num) >= 1e9:
            return f"{num/1e9:.2f}B"
        elif abs(num) >= 1e6:
            return f"{num/1e6:.2f}M"
        elif abs(num) >= 1e3:
            return f"{num/1e3:.2f}K"
        else:
            return f"{num:.2f}"
    except:
        return str(num)


def format_currency(amount, currency="₹"):
    """
    Format amount as currency (Indian Rupee format)
    
    Args:
        amount (float): Amount to format
        currency (str): Currency symbol (default: ₹)
    
    Returns:
        str: Formatted currency string
    """
    try:
        # Indian numbering system (lakhs and crores)
        if amount >= 10000000:  # 1 crore
            return f"{currency}{amount/10000000:.2f} Cr"
        elif amount >= 100000:  # 1 lakh
            return f"{currency}{amount/100000:.2f} L"
        else:
            return f"{currency}{amount:,.2f}"
    except:
        return f"{currency}{amount}"


def calculate_returns(data, period="daily"):
    """
    Calculate returns for the given data
    
    Args:
        data (pd.DataFrame): Historical stock data
        period (str): Return period ('daily', 'weekly', 'monthly')
    
    Returns:
        pd.Series: Calculated returns
    """
    if data is None or data.empty:
        return None
    
    if period == "daily":
        returns = data['Close'].pct_change()
    elif period == "weekly":
        returns = data['Close'].pct_change(periods=5)
    elif period == "monthly":
        returns = data['Close'].pct_change(periods=21)
    else:
        returns = data['Close'].pct_change()
    
    return returns


def calculate_volatility(returns, window=21):
    """
    Calculate rolling volatility
    
    Args:
        returns (pd.Series): Return series
        window (int): Rolling window size
    
    Returns:
        pd.Series: Volatility series
    """
    if returns is None:
        return None
    
    volatility = returns.rolling(window=window).std() * (252 ** 0.5)
    return volatility
