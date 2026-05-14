"""
Analysis Engine — Technical, Fundamental & Risk Analysis
Provides institutional-grade analytics for the recommendation engine.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, List, Any
import config


# =============================================================================
# TECHNICAL ANALYSIS
# =============================================================================

def compute_technical_score(data: pd.DataFrame, current_price: float) -> Dict[str, Any]:
    """
    Compute a composite technical analysis score (0-100) from multiple indicators.
    
    Returns a dict with individual indicator signals, an overall score, and a summary.
    """
    if data is None or data.empty or len(data) < 30:
        return {"score": 50, "signals": {}, "summary": "Insufficient data"}

    close = data['Close'].values
    high = data['High'].values
    low = data['Low'].values
    volume = data['Volume'].values if 'Volume' in data.columns else None

    signals: Dict[str, Dict] = {}
    scores: List[float] = []

    # --- RSI ---
    rsi = _compute_rsi(close)
    if rsi is not None:
        rsi_val = rsi[-1]
        if rsi_val <= 30:
            sig, sc = "Oversold — Bullish", 80
        elif rsi_val <= 40:
            sig, sc = "Approaching Oversold", 65
        elif rsi_val >= 70:
            sig, sc = "Overbought — Bearish", 20
        elif rsi_val >= 60:
            sig, sc = "Approaching Overbought", 40
        else:
            sig, sc = "Neutral", 50
        signals["RSI"] = {"value": round(rsi_val, 2), "signal": sig, "score": sc}
        scores.append(sc)

    # --- MACD ---
    macd_line, signal_line, histogram = _compute_macd(close)
    if macd_line is not None:
        m, s, h = macd_line[-1], signal_line[-1], histogram[-1]
        prev_h = histogram[-2] if len(histogram) > 1 else h
        if prev_h < 0 and h > 0:
            sig, sc = "Bullish Crossover", 85
        elif prev_h > 0 and h < 0:
            sig, sc = "Bearish Crossover", 15
        elif m > s and h > 0:
            sig, sc = "Bullish", 65
        elif m < s and h < 0:
            sig, sc = "Bearish", 35
        else:
            sig, sc = "Neutral", 50
        signals["MACD"] = {"value": round(m, 4), "signal": sig, "score": sc}
        scores.append(sc)

    # --- Moving Averages ---
    sma_50 = _sma(close, 50)
    sma_200 = _sma(close, 200)
    ema_20 = _ema(close, 20)

    if sma_50 is not None and sma_200 is not None:
        s50, s200 = sma_50[-1], sma_200[-1]
        if s50 > s200:
            sig, sc = "Golden Cross Zone — Bullish", 70
        else:
            sig, sc = "Death Cross Zone — Bearish", 30
        # Trend proximity
        dist_pct = (current_price - s200) / s200 * 100 if s200 != 0 else 0
        signals["MA_Cross"] = {"value": f"SMA50={s50:.2f}, SMA200={s200:.2f}", "signal": sig, "score": sc,
                               "detail": f"Price is {dist_pct:+.1f}% from SMA200"}
        scores.append(sc)

    if ema_20 is not None:
        e20 = ema_20[-1]
        if current_price > e20:
            sig, sc = "Above EMA20 — Short-term Bullish", 60
        else:
            sig, sc = "Below EMA20 — Short-term Bearish", 40
        signals["EMA_20"] = {"value": round(e20, 2), "signal": sig, "score": sc}
        scores.append(sc)

    # --- Bollinger Bands ---
    bb_upper, bb_middle, bb_lower = _bollinger_bands(close)
    if bb_upper is not None:
        bbu, bbm, bbl = bb_upper[-1], bb_middle[-1], bb_lower[-1]
        if current_price >= bbu:
            sig, sc = "At Upper Band — Overbought", 25
        elif current_price <= bbl:
            sig, sc = "At Lower Band — Oversold", 75
        elif current_price > bbm:
            sig, sc = "Above Middle Band", 55
        else:
            sig, sc = "Below Middle Band", 45
        signals["Bollinger"] = {"value": f"U={bbu:.2f} M={bbm:.2f} L={bbl:.2f}", "signal": sig, "score": sc}
        scores.append(sc)

    # --- ADX ---
    adx = _compute_adx(high, low, close)
    if adx is not None:
        adx_val = adx[-1]
        if adx_val > 25:
            sig = "Strong Trend"
        else:
            sig = "Weak / No Trend"
        sc = 60 if adx_val > 25 else 40
        signals["ADX"] = {"value": round(adx_val, 2), "signal": sig, "score": sc}
        scores.append(sc)

    # --- OBV trend ---
    if volume is not None and len(volume) > 20:
        obv = _compute_obv(close, volume)
        obv_sma = _sma(obv, 20)
        if obv_sma is not None:
            if obv[-1] > obv_sma[-1]:
                sig, sc = "Volume supports uptrend", 65
            else:
                sig, sc = "Volume diverging — caution", 35
            signals["OBV"] = {"value": f"{obv[-1]:.0f}", "signal": sig, "score": sc}
            scores.append(sc)

    # --- ATR (volatility) ---
    atr = _compute_atr(high, low, close)
    if atr is not None:
        atr_val = atr[-1]
        atr_pct = atr_val / current_price * 100 if current_price else 0
        if atr_pct > 3:
            sig = "High Volatility"
        elif atr_pct > 1.5:
            sig = "Moderate Volatility"
        else:
            sig = "Low Volatility"
        signals["ATR"] = {"value": round(atr_val, 2), "signal": sig, "pct": round(atr_pct, 2)}

    # --- Composite ---
    overall_score = np.mean(scores) if scores else 50.0
    bullish_count = sum(1 for s in scores if s > 55)
    bearish_count = sum(1 for s in scores if s < 45)

    if overall_score >= 65:
        summary = "Strong Bullish Consensus"
    elif overall_score >= 55:
        summary = "Moderately Bullish"
    elif overall_score <= 35:
        summary = "Strong Bearish Consensus"
    elif overall_score <= 45:
        summary = "Moderately Bearish"
    else:
        summary = "Mixed / Neutral"

    return {
        "score": round(overall_score, 1),
        "signals": signals,
        "summary": summary,
        "bullish_count": bullish_count,
        "bearish_count": bearish_count,
        "total_indicators": len(scores),
    }


# =============================================================================
# FUNDAMENTAL ANALYSIS
# =============================================================================

def compute_fundamental_score(stock_info: Dict) -> Dict[str, Any]:
    """
    Evaluate fundamental health and return a score (0-100).
    Uses PE, PB, ROE, D/E, dividend yield, and growth metrics.
    """
    if not stock_info:
        return {"score": 50, "metrics": {}, "summary": "No fundamental data available"}

    metrics: Dict[str, Any] = {}
    scores: List[float] = []

    # PE ratio
    pe = stock_info.get('pe_ratio') or 0
    if pe > 0:
        if pe < 15:
            sc = 80
            label = "Undervalued"
        elif pe < 25:
            sc = 60
            label = "Fairly Valued"
        elif pe < 40:
            sc = 40
            label = "Slightly Overvalued"
        else:
            sc = 20
            label = "Overvalued"
        metrics["PE Ratio"] = {"value": round(pe, 2), "assessment": label, "score": sc}
        scores.append(sc)

    # PB ratio (from info if available)
    pb = stock_info.get('pb_ratio') or stock_info.get('priceToBook') or 0
    if pb > 0:
        if pb < 1:
            sc = 85
            label = "Deep Value"
        elif pb < 3:
            sc = 65
            label = "Reasonable"
        elif pb < 5:
            sc = 40
            label = "Premium"
        else:
            sc = 20
            label = "Expensive"
        metrics["PB Ratio"] = {"value": round(pb, 2), "assessment": label, "score": sc}
        scores.append(sc)

    # Dividend yield
    div_yield = stock_info.get('dividend_yield') or 0
    if div_yield and div_yield > 0:
        dy_pct = div_yield * 100 if div_yield < 1 else div_yield
        if dy_pct > 3:
            sc = 75
            label = "Attractive Yield"
        elif dy_pct > 1:
            sc = 55
            label = "Moderate Yield"
        else:
            sc = 40
            label = "Low Yield"
        metrics["Dividend Yield"] = {"value": f"{dy_pct:.2f}%", "assessment": label, "score": sc}
        scores.append(sc)

    # Beta (risk)
    beta = stock_info.get('beta') or 0
    if beta > 0:
        if beta < 0.8:
            sc = 70
            label = "Low Volatility"
        elif beta < 1.2:
            sc = 60
            label = "Market-aligned"
        elif beta < 1.5:
            sc = 45
            label = "Moderately Volatile"
        else:
            sc = 30
            label = "Highly Volatile"
        metrics["Beta"] = {"value": round(beta, 2), "assessment": label, "score": sc}
        scores.append(sc)

    # Market cap (quality proxy)
    market_cap = stock_info.get('market_cap') or 0
    if market_cap > 0:
        if market_cap >= 200e9:
            sc = 75
            label = "Mega Cap"
        elif market_cap >= 10e9:
            sc = 65
            label = "Large Cap"
        elif market_cap >= 2e9:
            sc = 50
            label = "Mid Cap"
        else:
            sc = 35
            label = "Small Cap"
        metrics["Market Cap"] = {"value": _fmt_large(market_cap), "assessment": label, "score": sc}
        scores.append(sc)

    # EPS
    eps = stock_info.get('eps') or stock_info.get('trailingEps') or 0
    if eps != 0:
        if eps > 0:
            sc = 65
            label = "Profitable"
        else:
            sc = 25
            label = "Unprofitable"
        metrics["EPS"] = {"value": f"₹{eps:.2f}", "assessment": label, "score": sc}
        scores.append(sc)

    # ROE
    roe = stock_info.get('roe') or stock_info.get('returnOnEquity') or 0
    if roe and roe != 0:
        roe_pct = roe * 100 if abs(roe) < 1 else roe
        if roe_pct > 20:
            sc = 80
            label = "Excellent"
        elif roe_pct > 10:
            sc = 60
            label = "Good"
        elif roe_pct > 0:
            sc = 40
            label = "Below Average"
        else:
            sc = 15
            label = "Negative"
        metrics["ROE"] = {"value": f"{roe_pct:.1f}%", "assessment": label, "score": sc}
        scores.append(sc)

    # Debt-to-Equity
    de = stock_info.get('debtToEquity') or 0
    if de > 0:
        de_ratio = de / 100 if de > 10 else de  # some APIs return as %
        if de_ratio < 0.5:
            sc = 80
            label = "Low Debt"
        elif de_ratio < 1:
            sc = 60
            label = "Moderate Debt"
        elif de_ratio < 2:
            sc = 40
            label = "High Debt"
        else:
            sc = 20
            label = "Very High Debt"
        metrics["Debt/Equity"] = {"value": f"{de_ratio:.2f}", "assessment": label, "score": sc}
        scores.append(sc)

    overall = np.mean(scores) if scores else 50.0

    if overall >= 65:
        summary = "Strong Fundamentals"
    elif overall >= 50:
        summary = "Decent Fundamentals"
    elif overall >= 35:
        summary = "Weak Fundamentals"
    else:
        summary = "Poor Fundamentals"

    return {
        "score": round(overall, 1),
        "metrics": metrics,
        "summary": summary,
    }


# =============================================================================
# RISK ANALYSIS
# =============================================================================

def compute_risk_score(data: pd.DataFrame, benchmark_data: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Compute risk metrics: volatility, Sharpe, Sortino, max drawdown, VaR.
    Returns a risk score (0-100 where higher = lower risk).
    """
    if data is None or data.empty or len(data) < 30:
        return {"score": 50, "metrics": {}, "summary": "Insufficient data", "risk_level": "Unknown"}

    close = data['Close'].values
    returns = np.diff(close) / close[:-1]

    metrics: Dict[str, Any] = {}
    scores: List[float] = []

    # Annualized volatility
    vol_daily = np.std(returns)
    vol_annual = vol_daily * np.sqrt(252)
    if vol_annual < 0.15:
        sc = 85
        label = "Low"
    elif vol_annual < 0.30:
        sc = 60
        label = "Moderate"
    elif vol_annual < 0.50:
        sc = 35
        label = "High"
    else:
        sc = 15
        label = "Very High"
    metrics["Volatility (Annual)"] = {"value": f"{vol_annual*100:.1f}%", "assessment": label, "score": sc}
    scores.append(sc)

    # Sharpe ratio (risk-free = 5%)
    mean_return_annual = np.mean(returns) * 252
    rf = 0.05
    sharpe = (mean_return_annual - rf) / (vol_annual) if vol_annual > 0 else 0
    if sharpe > 1.5:
        sc = 85
        label = "Excellent"
    elif sharpe > 0.5:
        sc = 65
        label = "Good"
    elif sharpe > 0:
        sc = 45
        label = "Below Average"
    else:
        sc = 20
        label = "Poor"
    metrics["Sharpe Ratio"] = {"value": f"{sharpe:.2f}", "assessment": label, "score": sc}
    scores.append(sc)

    # Sortino ratio
    downside_returns = returns[returns < 0]
    downside_std = np.std(downside_returns) * np.sqrt(252) if len(downside_returns) > 0 else vol_annual
    sortino = (mean_return_annual - rf) / downside_std if downside_std > 0 else 0
    if sortino > 2:
        sc = 85
    elif sortino > 1:
        sc = 65
    elif sortino > 0:
        sc = 45
    else:
        sc = 20
    metrics["Sortino Ratio"] = {"value": f"{sortino:.2f}", "assessment": "Higher is better", "score": sc}
    scores.append(sc)

    # Max drawdown
    cumulative = np.cumprod(1 + returns)
    peak = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - peak) / peak
    max_dd = np.min(drawdown)
    if abs(max_dd) < 0.1:
        sc = 85
        label = "Minimal"
    elif abs(max_dd) < 0.2:
        sc = 65
        label = "Moderate"
    elif abs(max_dd) < 0.35:
        sc = 40
        label = "Significant"
    else:
        sc = 15
        label = "Severe"
    metrics["Max Drawdown"] = {"value": f"{max_dd*100:.1f}%", "assessment": label, "score": sc}
    scores.append(sc)

    # Value at Risk (95%)
    var_95 = np.percentile(returns, 5)
    metrics["VaR (95%)"] = {"value": f"{var_95*100:.2f}%", "assessment": "Daily worst-case at 95% confidence"}

    overall = np.mean(scores) if scores else 50.0

    if overall >= 70:
        risk_level = "Low Risk"
    elif overall >= 50:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    return {
        "score": round(overall, 1),
        "metrics": metrics,
        "summary": f"{risk_level} — Volatility {vol_annual*100:.1f}%, Sharpe {sharpe:.2f}",
        "risk_level": risk_level,
    }


# =============================================================================
# SUPPORT / RESISTANCE
# =============================================================================

def compute_support_resistance(data: pd.DataFrame) -> Dict[str, Any]:
    """Compute key support and resistance levels."""
    if data is None or data.empty or len(data) < 20:
        return {}

    close = data['Close'].values
    high = data['High'].values
    low = data['Low'].values
    current = close[-1]

    # Pivot points (classic)
    h, l, c = high[-1], low[-1], close[-1]
    pivot = (h + l + c) / 3
    r1 = 2 * pivot - l
    s1 = 2 * pivot - h
    r2 = pivot + (h - l)
    s2 = pivot - (h - l)

    # Recent swing highs/lows
    recent_high = float(np.max(high[-20:]))
    recent_low = float(np.min(low[-20:]))
    
    # Fibonacci levels from recent range
    fib_range = recent_high - recent_low
    fib_levels = {
        "Fib 0.0% (High)": recent_high,
        "Fib 23.6%": recent_high - 0.236 * fib_range,
        "Fib 38.2%": recent_high - 0.382 * fib_range,
        "Fib 50.0%": recent_high - 0.500 * fib_range,
        "Fib 61.8%": recent_high - 0.618 * fib_range,
        "Fib 100% (Low)": recent_low,
    }

    return {
        "pivot": round(pivot, 2),
        "resistance_1": round(r1, 2),
        "resistance_2": round(r2, 2),
        "support_1": round(s1, 2),
        "support_2": round(s2, 2),
        "recent_high": round(recent_high, 2),
        "recent_low": round(recent_low, 2),
        "fibonacci": {k: round(v, 2) for k, v in fib_levels.items()},
    }


# =============================================================================
# PRIVATE HELPERS — numpy-based indicator computations
# =============================================================================

def _sma(arr: np.ndarray, window: int) -> Optional[np.ndarray]:
    if len(arr) < window:
        return None
    kernel = np.ones(window) / window
    return np.convolve(arr, kernel, mode='valid')


def _ema(arr: np.ndarray, window: int) -> Optional[np.ndarray]:
    if len(arr) < window:
        return None
    alpha = 2 / (window + 1)
    ema = np.zeros(len(arr))
    ema[0] = arr[0]
    for i in range(1, len(arr)):
        ema[i] = alpha * arr[i] + (1 - alpha) * ema[i - 1]
    return ema


def _compute_rsi(close: np.ndarray, period: int = 14) -> Optional[np.ndarray]:
    if len(close) < period + 1:
        return None
    deltas = np.diff(close)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.zeros(len(deltas))
    avg_loss = np.zeros(len(deltas))
    avg_gain[period - 1] = np.mean(gains[:period])
    avg_loss[period - 1] = np.mean(losses[:period])
    for i in range(period, len(deltas)):
        avg_gain[i] = (avg_gain[i - 1] * (period - 1) + gains[i]) / period
        avg_loss[i] = (avg_loss[i - 1] * (period - 1) + losses[i]) / period
    rs = np.where(avg_loss != 0, avg_gain / avg_loss, 100)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def _compute_macd(close: np.ndarray, fast: int = 12, slow: int = 26, signal: int = 9):
    if len(close) < slow + signal:
        return None, None, None
    ema_fast = _ema(close, fast)
    ema_slow = _ema(close, slow)
    macd_line = ema_fast - ema_slow
    signal_line = _ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def _bollinger_bands(close: np.ndarray, window: int = 20, num_std: float = 2.0):
    if len(close) < window:
        return None, None, None
    sma = pd.Series(close).rolling(window).mean().values
    std = pd.Series(close).rolling(window).std().values
    upper = sma + num_std * std
    lower = sma - num_std * std
    return upper, sma, lower


def _compute_adx(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> Optional[np.ndarray]:
    if len(close) < period * 2:
        return None
    tr1 = high[1:] - low[1:]
    tr2 = np.abs(high[1:] - close[:-1])
    tr3 = np.abs(low[1:] - close[:-1])
    tr = np.maximum(tr1, np.maximum(tr2, tr3))

    up_move = high[1:] - high[:-1]
    down_move = low[:-1] - low[1:]
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)

    atr = pd.Series(tr).rolling(period).mean().values
    plus_di = 100 * pd.Series(plus_dm).rolling(period).mean().values / np.where(atr == 0, 1, atr)
    minus_di = 100 * pd.Series(minus_dm).rolling(period).mean().values / np.where(atr == 0, 1, atr)

    dx = 100 * np.abs(plus_di - minus_di) / np.where((plus_di + minus_di) == 0, 1, plus_di + minus_di)
    adx = pd.Series(dx).rolling(period).mean().values
    return adx


def _compute_atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> Optional[np.ndarray]:
    if len(close) < period + 1:
        return None
    tr1 = high[1:] - low[1:]
    tr2 = np.abs(high[1:] - close[:-1])
    tr3 = np.abs(low[1:] - close[:-1])
    tr = np.maximum(tr1, np.maximum(tr2, tr3))
    atr = pd.Series(tr).rolling(period).mean().values
    # Pad to match original length
    atr = np.concatenate([[np.nan], atr])
    return atr


def _compute_obv(close: np.ndarray, volume: np.ndarray) -> np.ndarray:
    obv = np.zeros(len(close))
    for i in range(1, len(close)):
        if close[i] > close[i - 1]:
            obv[i] = obv[i - 1] + volume[i]
        elif close[i] < close[i - 1]:
            obv[i] = obv[i - 1] - volume[i]
        else:
            obv[i] = obv[i - 1]
    return obv


def _fmt_large(num: float) -> str:
    """Format a large number with suffix."""
    if abs(num) >= 1e12:
        return f"${num/1e12:.1f}T"
    elif abs(num) >= 1e9:
        return f"${num/1e9:.1f}B"
    elif abs(num) >= 1e6:
        return f"${num/1e6:.1f}M"
    return f"${num:,.0f}"

