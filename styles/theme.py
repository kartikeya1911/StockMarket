"""
QuantEdge — Premium Finance UI Theme
Professional dark-mode design inspired by MoneyControl & Bloomberg Terminal.
Deep navy base, electric cyan accents, clean data-dense layouts.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# CSS — Complete UI overhaul
# ---------------------------------------------------------------------------

PREMIUM_CSS = """
<style>
/* ===== Google Font ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ===== Root Variables ===== */
:root {
    --bg-primary: #0A0E27;
    --bg-secondary: #111633;
    --bg-tertiary: #161D45;
    --bg-card: rgba(15, 20, 50, 0.85);
    --bg-card-hover: rgba(20, 28, 65, 0.95);
    --text-primary: #E8EAF6;
    --text-secondary: #78909C;
    --text-muted: #546E7A;
    --accent-cyan: #00D4FF;
    --accent-green: #00C853;
    --accent-red: #FF5252;
    --accent-gold: #FFD740;
    --accent-blue: #448AFF;
    --accent-orange: #FF9100;
    --border: rgba(255, 255, 255, 0.06);
    --border-hover: rgba(0, 212, 255, 0.25);
    --glass: rgba(15, 20, 50, 0.85);
    --blur: 20px;
    --radius: 14px;
    --radius-sm: 8px;
    --radius-xs: 6px;
    --shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
    --shadow-hover: 0 8px 40px rgba(0, 212, 255, 0.08);
    --transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ===== Global ===== */
html, body, [data-testid="stAppViewContainer"], .main {
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif !important;
    color: var(--text-primary);
}

.main {
    padding: 0 0.5rem;
}

[data-testid="stAppViewContainer"] {
    background: var(--bg-primary) !important;
}

/* ===== Sidebar — Sleek finance panel ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080C22 0%, #0D1230 50%, #080C22 100%) !important;
    border-right: 1px solid rgba(0, 212, 255, 0.08);
}

[data-testid="stSidebar"] [data-testid="stMarkdown"] {
    color: var(--text-primary);
}

[data-testid="stSidebar"] .stRadio > div {
    gap: 1px;
}

[data-testid="stSidebar"] .stRadio > div > label {
    background: transparent;
    border-radius: var(--radius-sm);
    padding: 0.65rem 1rem !important;
    margin: 0 !important;
    transition: var(--transition);
    border: 1px solid transparent;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.01em;
}

[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(0, 212, 255, 0.06);
    border-color: rgba(0, 212, 255, 0.12);
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
[data-testid="stSidebar"] .stRadio > div > label[aria-checked="true"] {
    background: rgba(0, 212, 255, 0.08) !important;
    border-color: rgba(0, 212, 255, 0.3) !important;
    color: #00D4FF !important;
    font-weight: 600 !important;
    box-shadow: inset 3px 0 0 #00D4FF;
}

/* ===== Buttons — Cyan gradient ===== */
.stButton > button {
    background: linear-gradient(135deg, #00D4FF 0%, #0091EA 100%) !important;
    color: #0A0E27 !important;
    font-weight: 700;
    font-family: 'Inter', sans-serif;
    border-radius: var(--radius-sm);
    border: none !important;
    padding: 0.55rem 1.5rem;
    transition: var(--transition);
    box-shadow: 0 4px 16px rgba(0, 212, 255, 0.2);
    letter-spacing: 0.02em;
    font-size: 0.88rem;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 28px rgba(0, 212, 255, 0.35);
    filter: brightness(1.1);
}

.stButton > button:active {
    transform: translateY(0);
}

/* ===== Form Submit ===== */
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #00D4FF 0%, #0091EA 100%) !important;
    color: #0A0E27 !important;
    font-weight: 700;
    border-radius: var(--radius-sm);
    border: none !important;
    box-shadow: 0 4px 16px rgba(0, 212, 255, 0.2);
}

/* ===== Metrics — Finance card style ===== */
[data-testid="stMetric"] {
    background: var(--glass);
    backdrop-filter: blur(var(--blur));
    -webkit-backdrop-filter: blur(var(--blur));
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    transition: var(--transition);
}

[data-testid="stMetric"]:hover {
    border-color: var(--border-hover);
    box-shadow: var(--shadow-hover);
}

[data-testid="stMetricValue"] {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: -0.02em;
}

[data-testid="stMetricDelta"] {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
}

/* ===== Headings ===== */
h1 {
    font-weight: 800 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: -0.03em;
    color: var(--text-primary) !important;
}

h2 {
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em;
}

h3 {
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
}

/* ===== Expanders ===== */
[data-testid="stExpander"] {
    background: var(--glass);
    backdrop-filter: blur(var(--blur));
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    transition: var(--transition);
}

[data-testid="stExpander"]:hover {
    border-color: rgba(0, 212, 255, 0.15) !important;
}

/* ===== Inputs — Clean finance style ===== */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    border-radius: var(--radius-sm) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    background: rgba(10, 14, 39, 0.7) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    transition: var(--transition);
    font-size: 0.9rem;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.15) !important;
}

.stSelectbox > div > div {
    border-radius: var(--radius-sm) !important;
}

/* ===== Dataframe / Tables ===== */
[data-testid="stDataFrame"] {
    border-radius: var(--radius) !important;
    overflow: hidden;
}

/* ===== Tabs — Underline style ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: transparent;
    border-bottom: 1px solid var(--border);
    padding: 0;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 0;
    padding: 10px 20px;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    transition: var(--transition);
    border-bottom: 2px solid transparent;
    color: var(--text-secondary) !important;
    font-size: 0.88rem;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary) !important;
    background: transparent;
}

.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: var(--accent-cyan) !important;
    border-bottom: 2px solid var(--accent-cyan) !important;
    font-weight: 600;
}

/* ===== Scrollbar ===== */
::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}
::-webkit-scrollbar-track {
    background: var(--bg-primary);
}
::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 212, 255, 0.2);
}

/* ===== Divider ===== */
hr {
    border-color: var(--border) !important;
    margin: 1.2rem 0 !important;
}

/* ===== Alert boxes ===== */
.stAlert {
    border-radius: var(--radius-sm) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ===== Download Button ===== */
.stDownloadButton > button {
    background: rgba(15, 20, 50, 0.85) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 500;
    transition: var(--transition);
}

.stDownloadButton > button:hover {
    border-color: var(--accent-cyan) !important;
    background: rgba(0, 212, 255, 0.06) !important;
}

/* ===== Progress ===== */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-green)) !important;
    border-radius: 4px;
}

/* ===== Hide Streamlit defaults ===== */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

</style>
"""


# ---------------------------------------------------------------------------
# UI component helpers
# ---------------------------------------------------------------------------

def inject_css():
    """Inject the premium CSS into the Streamlit app."""
    st.html(PREMIUM_CSS)


def render_html(html: str):
    """Render raw HTML reliably using st.html() (Streamlit 1.33+).
    Falls back to st.markdown for older versions."""
    if hasattr(st, 'html'):
        st.html(html)
    else:
        st.markdown(html, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", icon: str = ""):
    """Render a clean page header with accent underline."""
    render_html(f"""
    <div style="margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.06);">
        <h1 style="
            color: #E8EAF6;
            font-size: 2rem;
            margin-bottom: 0.2rem;
            font-weight: 800;
            letter-spacing: -0.03em;
        ">{icon} {title}</h1>
        <p style="color: #78909C; font-size: 0.95rem; margin: 0;">{subtitle}</p>
    </div>
    """)


def market_ticker_bar(indices_data: dict):
    """Render a horizontal market indices bar (MoneyControl style)."""
    items_html = ""
    for name, data in indices_data.items():
        if data is None:
            continue
        price = data.get("price", 0)
        change = data.get("change", 0)
        pct = data.get("pct", 0)
        color = "#00C853" if change >= 0 else "#FF5252"
        arrow = "▲" if change >= 0 else "▼"
        items_html += f"""
        <div style="
            display: inline-flex; align-items: center; gap: 8px;
            padding: 6px 16px;
            border-right: 1px solid rgba(255,255,255,0.06);
        ">
            <span style="color: #78909C; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase;">{name}</span>
            <span style="color: #E8EAF6; font-size: 0.85rem; font-weight: 700; font-family: 'JetBrains Mono', monospace;">{price:,.2f}</span>
            <span style="color: {color}; font-size: 0.75rem; font-weight: 600; font-family: 'JetBrains Mono', monospace;">{arrow} {abs(change):,.2f} ({abs(pct):.2f}%)</span>
        </div>
        """

    render_html(f"""
    <div style="
        background: rgba(10, 14, 39, 0.95);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 10px;
        padding: 4px 0;
        margin-bottom: 1.2rem;
        overflow-x: auto;
        white-space: nowrap;
        display: flex;
        align-items: center;
    ">
        {items_html}
    </div>
    """)


def gradient_card(title: str, value: str, gradient: str = "linear-gradient(135deg, #00D4FF 0%, #0091EA 100%)", icon: str = ""):
    """Render a gradient KPI card."""
    return f"""
    <div style="
        background: {gradient};
        padding: 1.3rem;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 6px 24px rgba(0,0,0,0.3);
        transition: all 0.25s ease;
    ">
        <p style="color: rgba(255,255,255,0.85); margin: 0; font-size: 0.82rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase;">{icon} {title}</p>
        <h2 style="color: white; margin: 0.4rem 0 0 0; font-size: 1.8rem; font-weight: 800; letter-spacing: -0.02em;">{value}</h2>
    </div>
    """


def stat_card(label: str, value: str, change: str = "", change_color: str = "#00C853", sublabel: str = ""):
    """Render a compact stat card (MoneyControl style)."""
    change_html = f'<span style="color: {change_color}; font-size: 0.78rem; font-weight: 600; font-family: \'JetBrains Mono\', monospace;">{change}</span>' if change else ""
    sublabel_html = f'<p style="color: #546E7A; font-size: 0.72rem; margin: 2px 0 0 0;">{sublabel}</p>' if sublabel else ""
    return f"""
    <div style="
        background: rgba(15, 20, 50, 0.85);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 1rem 1.1rem;
        transition: all 0.25s ease;
    ">
        <p style="color: #78909C; margin: 0; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase;">{label}</p>
        <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 4px;">
            <span style="color: #E8EAF6; font-size: 1.3rem; font-weight: 700; font-family: 'JetBrains Mono', monospace;">{value}</span>
            {change_html}
        </div>
        {sublabel_html}
    </div>
    """


def glass_card(content: str, padding: str = "1.3rem"):
    """Render a glassmorphism card."""
    return f"""
    <div style="
        background: rgba(15, 20, 50, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: {padding};
        margin-bottom: 0.8rem;
        transition: all 0.25s ease;
    ">
        {content}
    </div>
    """


def section_header(title: str, subtitle: str = ""):
    """Render a section header with subtle styling."""
    sub_html = f'<span style="color: #546E7A; font-size: 0.82rem; margin-left: 10px;">{subtitle}</span>' if subtitle else ""
    render_html(f"""
    <div style="margin: 1.2rem 0 0.8rem 0; display: flex; align-items: baseline; gap: 6px;">
        <h3 style="color: #E8EAF6; font-size: 1.05rem; font-weight: 700; margin: 0; letter-spacing: -0.01em;">{title}</h3>
        {sub_html}
    </div>
    """)


def signal_badge(signal: str, color: str = "#00D4FF"):
    """Render a signal badge."""
    return f"""
    <span style="
        background: {color}15;
        color: {color};
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        border: 1px solid {color}30;
        display: inline-block;
        letter-spacing: 0.02em;
    ">{signal}</span>
    """


def recommendation_badge(recommendation: str):
    """Render a recommendation badge with appropriate color."""
    colors = {
        "Strong Buy": "#00C853",
        "Buy": "#00BFA5",
        "Hold": "#FFD740",
        "Sell": "#FF9100",
        "Strong Sell": "#FF5252",
    }
    color = colors.get(recommendation, "#78909C")
    return f"""
    <div style="
        background: {color}12;
        border: 2px solid {color};
        border-radius: 14px;
        padding: 1rem 2rem;
        text-align: center;
        margin: 0.8rem 0;
    ">
        <p style="color: {color}; font-size: 1.3rem; font-weight: 800; margin: 0; letter-spacing: 0.02em;">{recommendation}</p>
    </div>
    """


def score_gauge(label: str, score: float, max_score: float = 100):
    """Render a score bar."""
    pct = min(max(score / max_score * 100, 0), 100)
    if pct >= 60:
        color = "#00C853"
    elif pct >= 40:
        color = "#FFD740"
    else:
        color = "#FF5252"
    return f"""
    <div style="margin: 0.4rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
            <span style="color: #78909C; font-size: 0.78rem; font-weight: 500;">{label}</span>
            <span style="color: {color}; font-size: 0.78rem; font-weight: 700; font-family: 'JetBrains Mono', monospace;">{score:.1f}/{max_score:.0f}</span>
        </div>
        <div style="background: rgba(255,255,255,0.04); border-radius: 3px; height: 5px; overflow: hidden;">
            <div style="width: {pct}%; height: 100%; background: {color}; border-radius: 3px; transition: width 0.5s ease;"></div>
        </div>
    </div>
    """


def metric_row(label: str, value: str, color: str = "#E8EAF6"):
    """Simple label-value row."""
    return f"""
    <div style="display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.03);">
        <span style="color: #78909C; font-size: 0.84rem;">{label}</span>
        <span style="color: {color}; font-size: 0.84rem; font-weight: 600; font-family: 'JetBrains Mono', monospace;">{value}</span>
    </div>
    """


def data_table_row(cells: list, header: bool = False):
    """Render a table row with cells."""
    tag = "th" if header else "td"
    weight = "600" if header else "400"
    color = "#78909C" if header else "#E8EAF6"
    bg = "rgba(0,212,255,0.04)" if header else "transparent"
    cells_html = "".join(
        f'<{tag} style="padding: 8px 12px; color: {color}; font-weight: {weight}; font-size: 0.82rem; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.04);">{c}</{tag}>'
        for c in cells
    )
    return f'<tr style="background: {bg};">{cells_html}</tr>'
