"""
Stock Data Fetching and Management Module
Handles all operations related to fetching and processing stock data using yfinance
"""

import time
import yfinance as yf
import pandas as pd
import streamlit as st
import requests
from requests.exceptions import HTTPError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime, timedelta
import config


def _get_retry_session():
    """Shared requests session with retry/backoff to reduce 429s."""
    session = requests.Session()
    retry = Retry(
        total=6,
        backoff_factor=2.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],
        respect_retry_after_header=True
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    })
    return session


YF_SESSION = _get_retry_session()

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
        self.ticker = ticker.strip().upper()
        self.stock = None
        self.info = None
        self.session = YF_SESSION

    def _with_retry(self, fn, *, attempts=4, backoff=1.5, label="call"):
        """Retry wrapper for yfinance calls that may hit 429s."""
        delay = backoff
        last_exc = None
        for _ in range(attempts):
            try:
                return fn()
            except Exception as exc:
                last_exc = exc
                if "429" not in str(exc):
                    break
                time.sleep(delay)
                delay *= 1.5
        raise last_exc if last_exc else Exception(f"Failed {label}")

    def _ensure_stock(self):
        """Instantiate yfinance Ticker with retry-capable session."""
        if self.stock is None:
            self.stock = yf.Ticker(self.ticker, session=self.session)
        return self.stock

    def _fetch_quote_json(self):
        """Hit Yahoo quote endpoint (no crumb) as fallback."""
        url = "https://query1.finance.yahoo.com/v7/finance/quote"
        # Use IN region for NSE/BSE tickers to reduce missing fields
        is_india = self.ticker.endswith((".NS", ".BO"))
        params = {
            "symbols": self.ticker,
            "region": "IN" if is_india else "US",
            "lang": "en-IN" if is_india else "en-US",
        }
        resp = self.session.get(url, params=params, timeout=10)
        if resp.status_code == 429:
            raise RuntimeError("Yahoo rate limit (429) on quote endpoint")
        resp.raise_for_status()
        data = resp.json()
        quotes = data.get("quoteResponse", {}).get("result", [])
        if not quotes:
            return {}
        return quotes[0]

    def _fetch_chart_df(self, range_="1y", interval="1d"):
        """Use Yahoo chart endpoint (avoids crumb) for history."""
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{self.ticker}"
        params = {"range": range_, "interval": interval, "includePrePost": False}
        resp = self.session.get(url, params=params, timeout=10)
        if resp.status_code == 429:
            raise RuntimeError("Yahoo rate limit (429) on chart endpoint")
        resp.raise_for_status()
        data = resp.json()
        result = data.get("chart", {}).get("result") or []
        if not result:
            return None
        r0 = result[0]
        timestamps = r0.get("timestamp") or []
        indicators = r0.get("indicators", {}).get("quote", [{}])[0]
        if not timestamps or not indicators:
            return None
        df = pd.DataFrame(indicators)
        df["Date"] = pd.to_datetime(timestamps, unit="s")
        cols = ["Date"] + [c for c in ["open", "high", "low", "close", "volume"] if c in df]
        df = df[cols]
        df.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"}, inplace=True)
        return df

    def _get_fast_info(self):
        """Use fast_info (avoids crumb endpoint) with retries."""
        self._ensure_stock()
        return self._with_retry(lambda: self.stock.fast_info, attempts=4, backoff=2.0, label="fast_info")
        
    def validate_ticker(self):
        """
        Validate if the ticker symbol is valid
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            price = None

            # First attempt fast_info to avoid Yahoo quote 401s
            try:
                fast = self._get_fast_info()
                price = fast.get("last_price") or fast.get("regular_market_price") or fast.get("previous_close")
            except Exception as e:
                if "429" in str(e):
                    st.warning("Yahoo rate limit hit while validating ticker. Please retry in a moment or switch network.")
                    return False
                # Fast-info failed; fall back to quote endpoint below

            # Prefer quote endpoint (no crumb); fallback to history chart if price missing
            try:
                if price is None:
                    q = self._fetch_quote_json()
                    price = q.get("regularMarketPrice") or q.get("postMarketPrice") or q.get("regularMarketPreviousClose")
            except Exception as e:
                if "429" in str(e):
                    st.warning("Yahoo rate limit hit while validating ticker. Please retry in a moment or switch network.")
                    return False
                if isinstance(e, HTTPError) and getattr(e.response, "status_code", None) == 401:
                    # Yahoo sometimes returns 401 without crumb; rely on chart endpoint below
                    price = None
                else:
                    raise

            if price is None:
                try:
                    hist = self._fetch_chart_df(range_="5d", interval="1d")
                except Exception as e:
                    if "429" in str(e):
                        st.warning("Yahoo rate limit hit while validating ticker. Please retry in a moment or switch network.")
                        return False
                    raise
                if hist is None or hist.empty:
                    return False
                price = float(hist["Close"].iloc[-1]) if "Close" in hist else None

            if price is None:
                return False

            self.info = {"regularMarketPrice": price}
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
            try:
                q = self._fetch_quote_json()
            except Exception as e:
                if "429" in str(e):
                    st.warning("Yahoo rate limit hit while fetching stock info. Please retry in a moment or switch network.")
                    return None
                if isinstance(e, HTTPError) and getattr(e.response, "status_code", None) == 401:
                    # Fall back to fast_info when quote endpoint blocks with 401
                    try:
                        fast = self._get_fast_info()
                        q = {
                            "regularMarketPrice": fast.get("last_price") or fast.get("regular_market_price"),
                            "regularMarketPreviousClose": fast.get("previous_close") or fast.get("regular_market_previous_close"),
                            "longName": self.ticker,
                            "shortName": self.ticker,
                        }
                    except Exception:
                        st.error("Unable to fetch stock info due to Yahoo 401 response.")
                        return None
                else:
                    raise
            price = q.get("regularMarketPrice") or q.get("postMarketPrice")
            previous_close = q.get("regularMarketPreviousClose") or q.get("postMarketPrice")
            day_high = q.get("regularMarketDayHigh")
            day_low = q.get("regularMarketDayLow")
            volume = q.get("regularMarketVolume")
            market_cap = q.get("marketCap")

            # Fallback to fast_info if any key price fields are missing/zero
            if (price in (None, 0)) or (previous_close in (None, 0)):
                try:
                    fast = self._get_fast_info()
                    price = price or fast.get("last_price") or fast.get("regular_market_price")
                    previous_close = previous_close or fast.get("previous_close") or fast.get("regular_market_previous_close")
                    day_high = day_high or fast.get("day_high") or fast.get("regular_market_day_high")
                    day_low = day_low or fast.get("day_low") or fast.get("regular_market_day_low")
                except Exception:
                    pass

            # Final fallback: last close from chart data
            if price in (None, 0) or previous_close in (None, 0):
                try:
                    for rng in ("5d", "1mo"):
                        hist = self._fetch_chart_df(range_=rng, interval="1d")
                        if hist is not None and not hist.empty and "Close" in hist:
                            last_close = float(hist["Close"].iloc[-1])
                            price = price or last_close
                            previous_close = previous_close or last_close
                            day_high = day_high or float(hist["High"].iloc[-1]) if "High" in hist else day_high
                            day_low = day_low or float(hist["Low"].iloc[-1]) if "Low" in hist else day_low
                            volume = volume or float(hist["Volume"].iloc[-1]) if "Volume" in hist else volume
                            break
                except Exception:
                    pass
            
            # Extract key information with fallbacks
            price = price or 0
            previous_close = previous_close or 0
            day_high = day_high or 0
            day_low = day_low or 0
            volume = volume or 0
            market_cap = market_cap or 0

            stock_info = {
                'symbol': self.ticker,
                'name': q.get('longName') or q.get('shortName') or self.ticker,
                'current_price': price,
                'previous_close': previous_close,
                'open': q.get('regularMarketOpen') or 0,
                'day_high': day_high,
                'day_low': day_low,
                'volume': volume,
                'market_cap': market_cap,
                '52_week_high': q.get('fiftyTwoWeekHigh') or 0,
                '52_week_low': q.get('fiftyTwoWeekLow') or 0,
                'pe_ratio': q.get('trailingPE') or 0,
                'dividend_yield': q.get('dividendYield') or 0,
                'beta': q.get('beta') or 0,
                'sector': q.get('sector') or 'N/A',
                'industry': q.get('industry') or 'N/A',
                'website': q.get('website') or 'N/A',
                'description': q.get('longBusinessSummary') or 'N/A'
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
            hist_data = self._with_retry(lambda: self._fetch_chart_df(range_=period, interval=interval), label="history")
            
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
            hist_data = self._with_retry(
                lambda: self._fetch_chart_df(range_="max", interval=interval).query("@start_date <= Date <= @end_date") if self._fetch_chart_df(range_="max", interval=interval) is not None else None,
                label="history-range"
            )
            
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
            current_price = None
            previous_close = None

            # 1) Try fast_info first
            try:
                fast = self._get_fast_info()
                fast_price_keys = [
                    'last_price', 'regular_market_price', 'lastPrice', 'regularMarketPrice'
                ]
                fast_prev_keys = [
                    'previous_close', 'regular_market_previous_close', 'previousClose', 'regularMarketPreviousClose'
                ]
                for k in fast_price_keys:
                    if fast.get(k) is not None:
                        current_price = fast.get(k)
                        break
                for k in fast_prev_keys:
                    if fast.get(k) is not None:
                        previous_close = fast.get(k)
                        break
            except Exception:
                pass

            # 2) Fall back to quote endpoint if needed
            if current_price in (None, 0) or previous_close in (None, 0):
                try:
                    q = self._fetch_quote_json()
                    current_price = current_price or q.get('regularMarketPrice') or q.get('postMarketPrice')
                    previous_close = previous_close or q.get('regularMarketPreviousClose') or q.get('postMarketPrice')
                except Exception:
                    pass

            # 3) Fall back to last close from chart data
            if current_price in (None, 0) or previous_close in (None, 0):
                try:
                    hist = self._fetch_chart_df(range_="5d", interval="1d")
                    if hist is not None and not hist.empty:
                        last_close = float(hist['Close'].iloc[-1]) if 'Close' in hist else None
                        current_price = current_price or last_close
                        previous_close = previous_close or last_close
                except Exception:
                    pass

            # If still missing, signal failure
            if current_price in (None, 0) or previous_close in (None, 0):
                st.warning(f"Unable to fetch live price for {self.ticker}. Yahoo may be throttling or returning incomplete data.")
                return None

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
            self._ensure_stock()
            
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
            self._ensure_stock()
            
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
            self._ensure_stock()
            
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
            self._ensure_stock()
            
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
