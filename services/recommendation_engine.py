"""
AI Recommendation Engine — Weighted Multi-Factor Scoring
Produces explainable Buy/Hold/Sell recommendations with confidence metrics.
"""

from typing import Dict, Any, Optional, List
import numpy as np
import config


def generate_recommendation(
    technical_result: Dict[str, Any],
    fundamental_result: Dict[str, Any],
    sentiment_result: Optional[Dict[str, Any]],
    prediction_result: Optional[Dict[str, Any]],
    risk_result: Dict[str, Any],
    current_price: float,
    support_resistance: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Generate an explainable AI recommendation by combining multiple analysis dimensions.

    Weights (from config):
        Technical  → 30%
        Fundamental → 25%
        Sentiment  → 15%
        AI Prediction → 20%
        Risk       → 10%

    Returns a comprehensive recommendation dict.
    """
    weights = config.RECOMMENDATION_WEIGHTS

    # --- Normalize scores to 0-100 ---
    tech_score = technical_result.get("score", 50)
    fund_score = fundamental_result.get("score", 50)

    # Sentiment
    if sentiment_result and sentiment_result.get("avg_polarity") is not None:
        # Map polarity [-1, 1] to [0, 100]
        sent_score = (sentiment_result["avg_polarity"] + 1) * 50
    else:
        sent_score = 50  # neutral

    # AI Prediction
    if prediction_result and prediction_result.get("predicted_change_pct") is not None:
        pct = prediction_result["predicted_change_pct"]
        # Map predicted change: +10% → 90, -10% → 10, clamped
        pred_score = np.clip(50 + pct * 4, 5, 95)
        pred_confidence = prediction_result.get("confidence", 0.5)
    else:
        pred_score = 50
        pred_confidence = 0

    # Risk (score is already 0-100 where higher = lower risk = more favorable)
    risk_score = risk_result.get("score", 50)

    # --- Weighted composite ---
    composite = (
        tech_score * weights["technical"] +
        fund_score * weights["fundamental"] +
        sent_score * weights["sentiment"] +
        pred_score * weights["ai_prediction"] +
        risk_score * weights["risk"]
    )

    # --- Determine recommendation ---
    if composite >= 75:
        recommendation = "Strong Buy"
    elif composite >= 60:
        recommendation = "Buy"
    elif composite >= 40:
        recommendation = "Hold"
    elif composite >= 25:
        recommendation = "Sell"
    else:
        recommendation = "Strong Sell"

    # --- Confidence ---
    # Higher when scores agree, lower when they diverge
    all_scores = [tech_score, fund_score, sent_score, pred_score, risk_score]
    score_std = np.std(all_scores)
    agreement_confidence = max(0, 100 - score_std * 2)

    # Factor in data availability
    data_completeness = sum([
        1 if technical_result.get("total_indicators", 0) >= 3 else 0.5,
        1 if len(fundamental_result.get("metrics", {})) >= 3 else 0.5,
        1 if sentiment_result and sentiment_result.get("total_articles", 0) >= 3 else 0.3,
        pred_confidence,
        1 if risk_result.get("risk_level") != "Unknown" else 0.3,
    ]) / 5.0

    overall_confidence = round(agreement_confidence * data_completeness, 1)

    # --- Entry/Exit/Stop-loss ---
    entry_zone = None
    exit_zone = None
    stop_loss = None
    if support_resistance:
        s1 = support_resistance.get("support_1", current_price * 0.97)
        r1 = support_resistance.get("resistance_1", current_price * 1.03)
        s2 = support_resistance.get("support_2", current_price * 0.95)
        entry_zone = f"₹{s1:,.2f} — ₹{current_price:,.2f}"
        exit_zone = f"₹{current_price:,.2f} — ₹{r1:,.2f}"
        stop_loss = f"₹{s2:,.2f}"

    # --- Risk/Reward ---
    risk_level = risk_result.get("risk_level", "Unknown")
    if recommendation in ("Strong Buy", "Buy"):
        risk_reward = "Favorable"
    elif recommendation == "Hold":
        risk_reward = "Neutral"
    else:
        risk_reward = "Unfavorable"

    # --- Investment suitability ---
    suitability = _determine_suitability(composite, risk_score, tech_score, fund_score)

    # --- Explanation ---
    reasons = _build_explanation(
        tech_score, fund_score, sent_score, pred_score, risk_score,
        technical_result, fundamental_result, sentiment_result, prediction_result, risk_result,
    )

    return {
        "recommendation": recommendation,
        "composite_score": round(composite, 1),
        "confidence": overall_confidence,
        "risk_level": risk_level,
        "risk_reward": risk_reward,
        "entry_zone": entry_zone,
        "exit_zone": exit_zone,
        "stop_loss": stop_loss,
        "suitability": suitability,
        "breakdown": {
            "Technical": {"score": round(tech_score, 1), "weight": f"{weights['technical']*100:.0f}%",
                          "summary": technical_result.get("summary", "N/A")},
            "Fundamental": {"score": round(fund_score, 1), "weight": f"{weights['fundamental']*100:.0f}%",
                            "summary": fundamental_result.get("summary", "N/A")},
            "Sentiment": {"score": round(sent_score, 1), "weight": f"{weights['sentiment']*100:.0f}%",
                          "summary": sentiment_result.get("overall_sentiment", "Neutral") if sentiment_result else "N/A"},
            "AI Prediction": {"score": round(pred_score, 1), "weight": f"{weights['ai_prediction']*100:.0f}%",
                              "summary": f"{prediction_result.get('predicted_change_pct', 0):+.1f}% predicted" if prediction_result else "N/A"},
            "Risk": {"score": round(risk_score, 1), "weight": f"{weights['risk']*100:.0f}%",
                     "summary": risk_result.get("summary", "N/A")},
        },
        "reasons": reasons,
    }


def _determine_suitability(composite: float, risk_score: float, tech_score: float, fund_score: float) -> List[str]:
    """Determine which investment styles this stock suits."""
    styles = []
    if tech_score >= 65 and composite >= 60:
        styles.append("Swing Trade")
    if tech_score >= 70:
        styles.append("Intraday")
    if fund_score >= 60 and risk_score >= 55:
        styles.append("Long-term Investing")
    if risk_score >= 70 and fund_score >= 55:
        styles.append("Defensive Investing")
    if composite >= 70 and risk_score < 40:
        styles.append("Speculative Trade")
    if not styles:
        styles.append("Hold / Monitor")
    return styles


def _build_explanation(
    tech_score, fund_score, sent_score, pred_score, risk_score,
    tech_result, fund_result, sent_result, pred_result, risk_result,
) -> List[str]:
    """Build human-readable explanation of the recommendation."""
    reasons = []

    # Technical
    if tech_score >= 65:
        reasons.append(f"📊 Technical indicators show {tech_result.get('summary', 'bullish')} signals "
                       f"({tech_result.get('bullish_count', 0)}/{tech_result.get('total_indicators', 0)} bullish)")
    elif tech_score <= 35:
        reasons.append(f"📊 Technical indicators are predominantly bearish "
                       f"({tech_result.get('bearish_count', 0)}/{tech_result.get('total_indicators', 0)} bearish)")
    else:
        reasons.append("📊 Technical indicators show mixed/neutral signals")

    # Fundamental
    if fund_score >= 65:
        reasons.append(f"🏢 Strong fundamentals — {fund_result.get('summary', 'healthy financials')}")
    elif fund_score <= 35:
        reasons.append(f"🏢 Weak fundamentals — {fund_result.get('summary', 'concerns present')}")
    else:
        reasons.append(f"🏢 Fundamental analysis: {fund_result.get('summary', 'average')}")

    # Sentiment
    if sent_result:
        overall_sent = sent_result.get("overall_sentiment", "Neutral")
        if sent_score >= 65:
            reasons.append(f"📰 News sentiment is {overall_sent.lower()} — positive market perception")
        elif sent_score <= 35:
            reasons.append(f"📰 News sentiment is {overall_sent.lower()} — exercise caution")
        else:
            reasons.append(f"📰 News sentiment is neutral/mixed")

    # Prediction
    if pred_result and pred_result.get("predicted_change_pct") is not None:
        pct = pred_result["predicted_change_pct"]
        if pct > 3:
            reasons.append(f"🤖 AI model predicts {pct:+.1f}% upside over 30 days")
        elif pct < -3:
            reasons.append(f"🤖 AI model predicts {pct:+.1f}% downside over 30 days")
        else:
            reasons.append(f"🤖 AI model predicts relatively flat movement ({pct:+.1f}%)")

    # Risk
    risk_level = risk_result.get("risk_level", "Unknown")
    if risk_score >= 65:
        reasons.append(f"🛡️ {risk_level} — favorable risk-adjusted returns")
    elif risk_score <= 35:
        reasons.append(f"🛡️ {risk_level} — elevated risk profile")
    else:
        reasons.append(f"🛡️ {risk_level}")

    return reasons

