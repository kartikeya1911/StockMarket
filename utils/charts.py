"""
QuantEdge — Premium Chart Module
Dark-themed Plotly visualizations with professional finance styling.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import config

# Common layout overrides
_GRID = "rgba(255,255,255,0.03)"

def _layout(**overrides):
    """Build a layout dict, merging axis overrides with defaults."""
    base = dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#E8EAF6", size=12),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    xa = dict(gridcolor=_GRID, showgrid=True, zeroline=False)
    ya = dict(gridcolor=_GRID, showgrid=True, zeroline=False)
    xa.update(overrides.pop('xaxis', {}))
    ya.update(overrides.pop('yaxis', {}))
    base['xaxis'] = xa
    base['yaxis'] = ya
    base.update(overrides)
    return base


def create_line_chart(data, x_col='Date', y_col='Close', title='Stock Price'):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data[x_col], y=data[y_col], mode='lines', name=y_col,
        line=dict(color="#00D4FF", width=2),
        fill='tozeroy', fillcolor='rgba(0,212,255,0.06)',
    ))
    fig.update_layout(**_layout(title=title, height=480,
                               yaxis_title='Price (₹)'))
    return fig


def create_candlestick_chart(data, title='Candlestick Chart'):
    fig = go.Figure(data=[go.Candlestick(
        x=data['Date'], open=data['Open'], high=data['High'],
        low=data['Low'], close=data['Close'], name='OHLC',
        increasing_line_color='#00C853', decreasing_line_color='#FF5252',
        increasing_fillcolor='#00C853', decreasing_fillcolor='#FF5252',
    )])
    fig.update_layout(**_layout(title=title, height=500,
                               xaxis_rangeslider_visible=False, yaxis_title='Price (₹)'))
    return fig


def create_volume_chart(data, title='Trading Volume'):
    colors = ['#FF5252' if row['Close'] < row['Open'] else '#00C853'
              for _, row in data.iterrows()]
    fig = go.Figure(data=[go.Bar(
        x=data['Date'], y=data['Volume'], marker_color=colors, name='Volume',
        opacity=0.7,
    )])
    fig.update_layout(**_layout(title=title, height=280, yaxis_title='Volume'))
    return fig


def create_ma_chart(data, ma_columns=['SMA_50', 'SMA_200'], title='Moving Averages'):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Date'], y=data['Close'], mode='lines', name='Price',
        line=dict(color='#E8EAF6', width=1.5),
    ))
    colors = ['#FFD740', '#FF5252', '#00D4FF', '#00C853']
    for i, col in enumerate(ma_columns):
        if col in data.columns:
            fig.add_trace(go.Scatter(
                x=data['Date'], y=data[col], mode='lines', name=col,
                line=dict(color=colors[i % len(colors)], width=2),
            ))
    fig.update_layout(**_layout(title=title, height=480, yaxis_title='Price (₹)'))
    return fig


def create_rsi_chart(data, rsi_col='RSI', title='RSI Indicator'):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Date'], y=data[rsi_col], mode='lines', name='RSI',
        line=dict(color='#00D4FF', width=2),
    ))
    fig.add_hrect(y0=70, y1=100, fillcolor="rgba(255,82,82,0.06)", line_width=0)
    fig.add_hrect(y0=0, y1=30, fillcolor="rgba(0,200,83,0.06)", line_width=0)
    fig.add_hline(y=70, line_dash="dash", line_color="rgba(255,82,82,0.4)",
                  annotation_text="Overbought", annotation_font_color="#FF5252")
    fig.add_hline(y=30, line_dash="dash", line_color="rgba(0,200,83,0.4)",
                  annotation_text="Oversold", annotation_font_color="#00C853")
    fig.update_layout(**_layout(title=title, height=350,
                               yaxis=dict(range=[0, 100], title='RSI')))
    return fig


def create_macd_chart(data, title='MACD Indicator'):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Date'], y=data['MACD'], mode='lines', name='MACD',
        line=dict(color='#00D4FF', width=2),
    ))
    fig.add_trace(go.Scatter(
        x=data['Date'], y=data['MACD_Signal'], mode='lines', name='Signal',
        line=dict(color='#FFD740', width=2),
    ))
    colors = ['#00C853' if v >= 0 else '#FF5252' for v in data['MACD_Histogram']]
    fig.add_trace(go.Bar(
        x=data['Date'], y=data['MACD_Histogram'], name='Histogram',
        marker_color=colors, opacity=0.6,
    ))
    fig.update_layout(**_layout(title=title, height=380, yaxis_title='MACD'))
    return fig


def create_bollinger_bands_chart(data, title='Bollinger Bands'):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Date'], y=data['BB_Upper'], mode='lines', name='Upper',
        line=dict(color='rgba(255,82,82,0.4)', width=1, dash='dash'),
    ))
    fig.add_trace(go.Scatter(
        x=data['Date'], y=data['BB_Lower'], mode='lines', name='Lower',
        line=dict(color='rgba(0,200,83,0.4)', width=1, dash='dash'),
        fill='tonexty', fillcolor='rgba(0,212,255,0.04)',
    ))
    fig.add_trace(go.Scatter(
        x=data['Date'], y=data['BB_Middle'], mode='lines', name='SMA',
        line=dict(color='#FFD740', width=1.5),
    ))
    fig.add_trace(go.Scatter(
        x=data['Date'], y=data['Close'], mode='lines', name='Price',
        line=dict(color='#E8EAF6', width=1.5),
    ))
    fig.update_layout(**_layout(title=title, height=480, yaxis_title='Price (₹)'))
    return fig


def create_prediction_chart(historical_data, predictions, title='Price Prediction',
                            confidence_band=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=historical_data['Date'], y=historical_data['Close'],
        mode='lines', name='Historical',
        line=dict(color='#00D4FF', width=2),
    ))
    if predictions is not None and not predictions.empty:
        fig.add_trace(go.Scatter(
            x=predictions['Date'], y=predictions['Predicted_Close'],
            mode='lines', name='Predicted',
            line=dict(color='#00C853', width=2, dash='dash'),
        ))
        if confidence_band is not None:
            fig.add_trace(go.Scatter(
                x=predictions['Date'], y=confidence_band['upper'],
                mode='lines', name='Upper CI', line=dict(width=0), showlegend=False,
            ))
            fig.add_trace(go.Scatter(
                x=predictions['Date'], y=confidence_band['lower'],
                mode='lines', name='Lower CI', line=dict(width=0),
                fill='tonexty', fillcolor='rgba(0,200,83,0.06)', showlegend=False,
            ))
    fig.update_layout(**_layout(title=title, height=500, yaxis_title='Price (₹)'))
    return fig


def create_portfolio_allocation_chart(allocation_data):
    colors = ['#00D4FF', '#00C853', '#FFD740', '#FF5252', '#448AFF',
              '#FF9100', '#00BFA5', '#7C4DFF', '#E040FB', '#78909C']
    fig = px.pie(
        allocation_data, values='Current_Value', names='Ticker',
        title='Portfolio Allocation', hole=0.5,
        color_discrete_sequence=colors,
    )
    fig.update_traces(textposition='inside', textinfo='percent+label',
                      textfont_size=11)
    fig.update_layout(**_layout(height=400, showlegend=False))
    return fig


def create_sentiment_chart(sentiment_data):
    labels = ['Positive', 'Negative', 'Neutral']
    values = [
        sentiment_data.get('positive_count', 0),
        sentiment_data.get('negative_count', 0),
        sentiment_data.get('neutral_count', 0),
    ]
    colors = ['#00C853', '#FF5252', '#78909C']
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values,
        marker=dict(colors=colors), hole=0.5,
        textinfo='percent+label', textfont_size=11,
    )])
    fig.update_layout(**_layout(title='Sentiment Distribution', height=380))
    return fig


def create_score_radar(breakdown: dict, title='Analysis Breakdown'):
    """Create a radar chart from recommendation breakdown scores."""
    categories = list(breakdown.keys())
    values = [breakdown[c]["score"] for c in categories]
    values.append(values[0])
    categories.append(categories[0])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values, theta=categories, fill='toself',
        fillcolor='rgba(0,212,255,0.15)',
        line=dict(color='#00D4FF', width=2),
        name='Score',
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(255,255,255,0.06)',
                            tickfont=dict(size=10, color='#546E7A')),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.06)',
                             tickfont=dict(size=11, color='#E8EAF6')),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="#E8EAF6"),
        title=title, height=400,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    return fig


def create_risk_gauge(score: float, title='Risk Score'):
    """Create a gauge chart for risk visualization."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title=dict(text=title, font=dict(size=14, color='#E8EAF6')),
        number=dict(font=dict(size=28, color='#E8EAF6')),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor='#546E7A'),
            bar=dict(color='#00D4FF'),
            bgcolor='rgba(0,0,0,0)',
            borderwidth=0,
            steps=[
                dict(range=[0, 30], color='rgba(255,82,82,0.15)'),
                dict(range=[30, 60], color='rgba(255,215,64,0.15)'),
                dict(range=[60, 100], color='rgba(0,200,83,0.15)'),
            ],
            threshold=dict(line=dict(color='#FFD740', width=2), value=score),
        ),
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif"),
        height=250, margin=dict(l=20, r=20, t=50, b=10),
    )
    return fig
