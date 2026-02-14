"""
News Fetching Module
Fetches stock-related news from various sources
"""

import requests
import streamlit as st
from datetime import datetime, timedelta
import config

class NewsFetcher:
    """
    Class to fetch news articles for stocks
    """
    
    def __init__(self, api_key=None):
        """
        Initialize News Fetcher
        
        Args:
            api_key (str): NewsAPI key
        """
        self.api_key = api_key or config.NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2/everything"
    
    def fetch_stock_news(self, ticker, days_back=7, max_articles=10):
        """
        Fetch news articles for a specific stock
        
        Args:
            ticker (str): Stock ticker symbol
            days_back (int): Number of days to look back
            max_articles (int): Maximum number of articles
        
        Returns:
            list: List of news articles
        """
        try:
            if self.api_key == "YOUR_API_KEY_HERE":
                return self._get_sample_news(ticker)
            
            # Remove exchange suffix for better news search
            # Indian stocks: .NS (NSE), .BO (BSE)
            # US stocks typically don't have suffixes
            search_ticker = ticker.split('.')[0]  # Remove .NS, .BO, etc.
            
            # Try to get company name for better search results
            try:
                from utils.stock_data import StockDataFetcher
                fetcher = StockDataFetcher(ticker)
                stock_info = fetcher.get_stock_info()
                if stock_info and stock_info.get('name'):
                    # Use company name for more relevant news
                    search_query = stock_info['name']
                else:
                    search_query = search_ticker
            except:
                search_query = search_ticker
            
            # Calculate date range
            to_date = datetime.now()
            from_date = to_date - timedelta(days=days_back)
            
            # Prepare parameters
            params = {
                'q': search_query,
                'from': from_date.strftime('%Y-%m-%d'),
                'to': to_date.strftime('%Y-%m-%d'),
                'language': config.NEWS_LANGUAGE,
                'sortBy': 'publishedAt',
                'pageSize': max_articles,
                'apiKey': self.api_key
            }
            
            # Make API request
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('articles', [])
            else:
                st.warning(f"News API returned status code: {response.status_code}")
                return self._get_sample_news(ticker)
        
        except Exception as e:
            st.warning(f"Unable to fetch news: {str(e)}")
            return self._get_sample_news(ticker)
    
    def _get_sample_news(self, ticker):
        """
        Get sample news articles (fallback when API is not available)
        
        Args:
            ticker (str): Stock ticker
        
        Returns:
            list: Sample news articles
        """
        # Remove exchange suffix for display
        display_ticker = ticker.split('.')[0]
        
        return [
            {
                'title': f'{display_ticker} Stock Analysis and Market Trends',
                'description': 'Market analysts discuss recent performance and future outlook.',
                'url': '#',
                'publishedAt': datetime.now().isoformat(),
                'source': {'name': 'Sample News'}
            },
            {
                'title': f'Investment Outlook for {display_ticker}',
                'description': 'Experts share insights on investment strategies.',
                'url': '#',
                'publishedAt': (datetime.now() - timedelta(days=1)).isoformat(),
                'source': {'name': 'Sample News'}
            },
            {
                'title': f'{display_ticker} Quarterly Earnings Report',
                'description': 'Company releases quarterly financial results.',
                'url': '#',
                'publishedAt': (datetime.now() - timedelta(days=2)).isoformat(),
                'source': {'name': 'Sample News'}
            }
        ]


@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_cached_news(ticker, days_back=7):
    """
    Cached function to fetch news
    
    Args:
        ticker (str): Stock ticker
        days_back (int): Days to look back
    
    Returns:
        list: News articles
    """
    fetcher = NewsFetcher()
    return fetcher.fetch_stock_news(ticker, days_back)
