"""
Chart Creation Module
Creates interactive charts using Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import config

def create_line_chart(data, x_col='Date', y_col='Close', title='Stock Price'):
    """
    Create a simple line chart
    
    Args:
        data (pd.DataFrame): Data to plot
        x_col (str): Column for x-axis
        y_col (str): Column for y-axis
        title (str): Chart title
    
    Returns:
        plotly figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data[x_col],
        y=data[y_col],
        mode='lines',
        name=y_col,
        line=dict(color=config.CHART_COLORS['primary'], width=2)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Price ($)',
        template=config.CHART_TEMPLATE,
        hovermode='x unified',
        height=500
    )
    
    return fig


def create_candlestick_chart(data, title='Candlestick Chart'):
    """
    Create candlestick chart
    
    Args:
        data (pd.DataFrame): OHLC data
        title (str): Chart title
    
    Returns:
        plotly figure
    """
    fig = go.Figure(data=[go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='OHLC'
    )])
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Price (₹)',
        template=config.CHART_TEMPLATE,
        xaxis_rangeslider_visible=False,
        height=500
    )
    
    return fig


def create_volume_chart(data, title='Trading Volume'):
    """
    Create volume bar chart
    
    Args:
        data (pd.DataFrame): Data with Volume column
        title (str): Chart title
    
    Returns:
        plotly figure
    """
    colors = ['red' if row['Close'] < row['Open'] else 'green' 
              for _, row in data.iterrows()]
    
    fig = go.Figure(data=[go.Bar(
        x=data['Date'],
        y=data['Volume'],
        marker_color=colors,
        name='Volume'
    )])
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Volume',
        template=config.CHART_TEMPLATE,
        height=300
    )
    
    return fig


def create_ma_chart(data, ma_columns=['SMA_50', 'SMA_200'], title='Moving Averages'):
    """
    Create chart with moving averages
    
    Args:
        data (pd.DataFrame): Data with MA columns
        ma_columns (list): List of MA column names
        title (str): Chart title
    
    Returns:
        plotly figure
    """
    fig = go.Figure()
    
    # Add close price
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color='blue', width=1)
    ))
    
    # Add moving averages
    colors = ['orange', 'red', 'purple', 'green']
    for i, ma_col in enumerate(ma_columns):
        if ma_col in data.columns:
            fig.add_trace(go.Scatter(
                x=data['Date'],
                y=data[ma_col],
                mode='lines',
                name=ma_col,
                line=dict(color=colors[i % len(colors)], width=2)
            ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Price ($)',
        template=config.CHART_TEMPLATE,
        hovermode='x unified',
        height=500
    )
    
    return fig


def create_rsi_chart(data, rsi_col='RSI', title='RSI Indicator'):
    """
    Create RSI chart with overbought/oversold levels
    
    Args:
        data (pd.DataFrame): Data with RSI column
        rsi_col (str): RSI column name
        title (str): Chart title
    
    Returns:
        plotly figure
    """
    fig = go.Figure()
    
    # Add RSI line
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data[rsi_col],
        mode='lines',
        name='RSI',
        line=dict(color='blue', width=2)
    ))
    
    # Add overbought line
    fig.add_hline(y=70, line_dash="dash", line_color="red", 
                  annotation_text="Overbought (70)")
    
    # Add oversold line
    fig.add_hline(y=30, line_dash="dash", line_color="green", 
                  annotation_text="Oversold (30)")
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='RSI',
        template=config.CHART_TEMPLATE,
        height=400
    )
    
    return fig


def create_macd_chart(data, title='MACD Indicator'):
    """
    Create MACD chart
    
    Args:
        data (pd.DataFrame): Data with MACD columns
        title (str): Chart title
    
    Returns:
        plotly figure
    """
    fig = go.Figure()
    
    # Add MACD line
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['MACD'],
        mode='lines',
        name='MACD',
        line=dict(color='blue', width=2)
    ))
    
    # Add Signal line
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['MACD_Signal'],
        mode='lines',
        name='Signal',
        line=dict(color='orange', width=2)
    ))
    
    # Add histogram
    colors = ['green' if val >= 0 else 'red' 
              for val in data['MACD_Histogram']]
    
    fig.add_trace(go.Bar(
        x=data['Date'],
        y=data['MACD_Histogram'],
        name='Histogram',
        marker_color=colors
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='MACD',
        template=config.CHART_TEMPLATE,
        height=400
    )
    
    return fig


def create_bollinger_bands_chart(data, title='Bollinger Bands'):
    """
    Create Bollinger Bands chart
    
    Args:
        data (pd.DataFrame): Data with BB columns
        title (str): Chart title
    
    Returns:
        plotly figure
    """
    fig = go.Figure()
    
    # Add upper band
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['BB_Upper'],
        mode='lines',
        name='Upper Band',
        line=dict(color='red', width=1, dash='dash')
    ))
    
    # Add middle band (SMA)
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['BB_Middle'],
        mode='lines',
        name='Middle Band (SMA)',
        line=dict(color='blue', width=2)
    ))
    
    # Add lower band
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['BB_Lower'],
        mode='lines',
        name='Lower Band',
        line=dict(color='green', width=1, dash='dash'),
        fill='tonexty'
    ))
    
    # Add close price
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color='black', width=1)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Price ($)',
        template=config.CHART_TEMPLATE,
        hovermode='x unified',
        height=500
    )
    
    return fig


def create_prediction_chart(historical_data, predictions, title='Price Prediction'):
    """
    Create chart showing historical and predicted prices
    
    Args:
        historical_data (pd.DataFrame): Historical data
        predictions (pd.DataFrame): Predicted data
        title (str): Chart title
    
    Returns:
        plotly figure
    """
    fig = go.Figure()
    
    # Add historical data
    fig.add_trace(go.Scatter(
        x=historical_data['Date'],
        y=historical_data['Close'],
        mode='lines',
        name='Historical Price',
        line=dict(color='blue', width=2)
    ))
    
    # Add predictions
    if predictions is not None and not predictions.empty:
        fig.add_trace(go.Scatter(
            x=predictions['Date'],
            y=predictions['Predicted_Close'],
            mode='lines',
            name='Predicted Price',
            line=dict(color='red', width=2, dash='dash')
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Price ($)',
        template=config.CHART_TEMPLATE,
        hovermode='x unified',
        height=500
    )
    
    return fig


def create_portfolio_allocation_chart(allocation_data):
    """
    Create portfolio allocation pie chart
    
    Args:
        allocation_data (pd.DataFrame): Allocation data
    
    Returns:
        plotly figure
    """
    fig = px.pie(
        allocation_data,
        values='Current_Value',
        names='Ticker',
        title='Portfolio Allocation',
        hole=0.3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    return fig


def create_sentiment_chart(sentiment_data):
    """
    Create sentiment distribution chart
    
    Args:
        sentiment_data (dict): Sentiment analysis results
    
    Returns:
        plotly figure
    """
    labels = ['Positive', 'Negative', 'Neutral']
    values = [
        sentiment_data['positive_count'],
        sentiment_data['negative_count'],
        sentiment_data['neutral_count']
    ]
    colors = ['green', 'red', 'gray']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole=0.3
    )])
    
    fig.update_layout(
        title='News Sentiment Distribution',
        height=400
    )
    
    return fig
