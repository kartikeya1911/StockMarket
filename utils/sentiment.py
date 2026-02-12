"""
Sentiment Analysis Module
Performs sentiment analysis on news articles and text
"""

from textblob import TextBlob
import streamlit as st

class SentimentAnalyzer:
    """
    Class to perform sentiment analysis
    """
    
    def __init__(self):
        """
        Initialize Sentiment Analyzer
        """
        pass
    
    def analyze_text(self, text):
        """
        Analyze sentiment of text
        
        Args:
            text (str): Text to analyze
        
        Returns:
            dict: Sentiment information
        """
        try:
            if not text or text.strip() == "":
                return {
                    'polarity': 0,
                    'subjectivity': 0,
                    'sentiment': 'Neutral',
                    'confidence': 0
                }
            
            # Create TextBlob object
            blob = TextBlob(text)
            
            # Get polarity and subjectivity
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Determine sentiment category
            if polarity > 0.1:
                sentiment = 'Positive'
            elif polarity < -0.1:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'
            
            # Calculate confidence
            confidence = abs(polarity)
            
            return {
                'polarity': polarity,
                'subjectivity': subjectivity,
                'sentiment': sentiment,
                'confidence': confidence
            }
        
        except Exception as e:
            st.error(f"Error analyzing sentiment: {str(e)}")
            return None
    
    def analyze_news_articles(self, articles):
        """
        Analyze sentiment of multiple news articles
        
        Args:
            articles (list): List of news articles
        
        Returns:
            dict: Aggregated sentiment analysis
        """
        try:
            if not articles:
                return None
            
            sentiments = []
            polarities = []
            
            for article in articles:
                # Combine title and description
                text = f"{article.get('title', '')} {article.get('description', '')}"
                
                # Analyze sentiment
                result = self.analyze_text(text)
                if result:
                    sentiments.append(result['sentiment'])
                    polarities.append(result['polarity'])
            
            if not sentiments:
                return None
            
            # Calculate aggregate metrics
            avg_polarity = sum(polarities) / len(polarities)
            
            # Count sentiment types
            positive_count = sentiments.count('Positive')
            negative_count = sentiments.count('Negative')
            neutral_count = sentiments.count('Neutral')
            
            # Determine overall sentiment
            if positive_count > negative_count and positive_count > neutral_count:
                overall_sentiment = 'Positive'
            elif negative_count > positive_count and negative_count > neutral_count:
                overall_sentiment = 'Negative'
            else:
                overall_sentiment = 'Neutral'
            
            return {
                'overall_sentiment': overall_sentiment,
                'avg_polarity': avg_polarity,
                'positive_count': positive_count,
                'negative_count': negative_count,
                'neutral_count': neutral_count,
                'total_articles': len(articles),
                'positive_percent': (positive_count / len(sentiments)) * 100,
                'negative_percent': (negative_count / len(sentiments)) * 100,
                'neutral_percent': (neutral_count / len(sentiments)) * 100
            }
        
        except Exception as e:
            st.error(f"Error analyzing articles: {str(e)}")
            return None
    
    def get_sentiment_recommendation(self, sentiment_data):
        """
        Get investment recommendation based on sentiment
        
        Args:
            sentiment_data (dict): Sentiment analysis results
        
        Returns:
            dict: Recommendation
        """
        try:
            if not sentiment_data:
                return None
            
            overall = sentiment_data['overall_sentiment']
            positive_pct = sentiment_data['positive_percent']
            negative_pct = sentiment_data['negative_percent']
            
            if overall == 'Positive' and positive_pct > 60:
                return {
                    'recommendation': 'Bullish',
                    'message': 'News sentiment is strongly positive. Market outlook appears favorable.',
                    'color': 'green'
                }
            elif overall == 'Positive':
                return {
                    'recommendation': 'Moderately Bullish',
                    'message': 'News sentiment is positive. Consider positive market conditions.',
                    'color': 'lightgreen'
                }
            elif overall == 'Negative' and negative_pct > 60:
                return {
                    'recommendation': 'Bearish',
                    'message': 'News sentiment is strongly negative. Exercise caution.',
                    'color': 'red'
                }
            elif overall == 'Negative':
                return {
                    'recommendation': 'Moderately Bearish',
                    'message': 'News sentiment is negative. Be cautious with investments.',
                    'color': 'orange'
                }
            else:
                return {
                    'recommendation': 'Neutral',
                    'message': 'News sentiment is mixed. No clear directional bias.',
                    'color': 'gray'
                }
        
        except Exception as e:
            return None
