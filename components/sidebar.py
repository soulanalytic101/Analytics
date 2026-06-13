"""
components/sidebar.py — Global CSS injection + sidebar renderer
"""

import streamlit as st

# ── Design tokens ─────────────────────────────────────────────────────────────
GLOBAL_CSS = """
<style>
/* ── Google Font import ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Playfair+Display:wght@700&display=swap');

/* ── CSS Variables ── */
:root {
    --bg-base:        #0a0b0f;
    --bg-surface:     #111318;
    --bg-elevated:    #181b23;
    --bg-overlay:     #1e2230;
    --border:         rgba(255,255,255,0.07);
    --border-active:  rgba(255,255,255,0.18);

    --text-primary:   #f0f2f8;
    --text-secondary: #8b90a4;
    --text-muted:     #4e5268;

    --accent-blue:    #4f8ef7;
    --accent-violet:  #9b74f5;
    --accent-teal:    #2ec4b6;
    --accent-amber:   #f5a623;
    --accent-rose:    #f06292;
    --accent-green:   #4caf7d;

    --gradient-hero:  linear-gradient(135deg, #4f8ef7 0%, #9b74f5 100%);
    --gradient-warm:  linear-gradient(135deg, #f5a623 0%, #f06292 100%);
    --gradient-cool:  linear-gradient(135deg, #2ec4b6 0%, #4f8ef7 100%);

    --radius-sm:  6px;
    --radius-md:  10px;
    --radius-lg:  16px;
    --radius-xl:  22px;

    --shadow-card: 0 1px 3px rgba(0,0,0,0.5), 0 8px 24px rgba(0,0,0,0.3);
    --shadow-glow: 0 0 0 1px rgba(79,142,247,0.15), 0 8px 32px rgba(79,142,247,0.08);

    --font-sans: 'DM Sans', sans-serif;
    --font-mono: 'DM Mono', monospace;
    --font-display: 'Playfair Display', serif;
}

/* ── Base reset ── */
html, body, [class*="css"] {
    font-family: var(--font-sans) !important;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

.main .block-container {
    padding: 2rem 2.5rem 4rem !important;
    max-width: 1600px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1.25rem !important;
}
[data-testid="stSidebarNav"] {
    display: block !important;       /* hide default nav; we use custom */
}

/* ── Headings ── */
h1, h2, h3, h4, h5 {
    font-family: var(--font-sans) !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em !important;
}

.hero-title {
    font-size: 2.4rem !important;
    font-weight: 700 !important;
    background: var(--gradient-hero);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin: 0 !important;
    line-height: 1.15 !important;
}
.hero-sub {
    color: var(--text-secondary);
    font-size: 1rem;
    margin-top: 0.4rem;
}

.logo-mark {
    font-size: 2.4rem;
    background: var(--gradient-hero);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
    padding-top: 0.25rem;
}

.page-header {
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--text-primary);
    margin-bottom: 0.2rem;
}
.page-sub {
    color: var(--text-secondary);
    font-size: 0.92rem;
    margin-bottom: 1.5rem;
}

/* ── KPI Card ── */
.kpi-card {
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.4rem 1.6rem;
    box-shadow: var(--shadow-card);
    transition: border-color 0.2s, transform 0.2s;
    position: relative;
    overflow: hidden;
}
.kpi-card:hover {
    border-color: var(--border-active);
    transform: translateY(-2px);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--gradient-hero);
    opacity: 0;
    transition: opacity 0.2s;
}
.kpi-card:hover::before { opacity: 1; }

.kpi-label {
    font-size: 0.73rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--text-primary);
    line-height: 1;
}
.kpi-delta {
    font-size: 0.8rem;
    margin-top: 0.5rem;
    font-weight: 500;
}
.kpi-delta.up   { color: var(--accent-green); }
.kpi-delta.down { color: var(--accent-rose); }
.kpi-icon {
    position: absolute;
    top: 1.2rem; right: 1.4rem;
    font-size: 1.5rem;
    opacity: 0.15;
}

/* ── Section card (chart wrapper) ── */
.section-card {
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    box-shadow: var(--shadow-card);
}
.section-title {
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-secondary);
    margin-bottom: 1rem;
}

/* ── Badge ── */
.badge {
    display: inline-block;
    padding: 0.2em 0.65em;
    border-radius: 100px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.04em;
}
.badge-blue   { background: rgba(79,142,247,0.15);  color: var(--accent-blue); }
.badge-green  { background: rgba(76,175,125,0.15);  color: var(--accent-green); }
.badge-amber  { background: rgba(245,166,35,0.15);  color: var(--accent-amber); }
.badge-rose   { background: rgba(240,98,146,0.15);  color: var(--accent-rose); }
.badge-violet { background: rgba(155,116,245,0.15); color: var(--accent-violet); }
.badge-teal   { background: rgba(46,196,182,0.15);  color: var(--accent-teal); }

/* ── Table tweaks ── */
[data-testid="stDataFrame"] { border-radius: var(--radius-md) !important; }
[data-testid="stDataFrame"] thead th {
    background: var(--bg-overlay) !important;
    color: var(--text-secondary) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
}

/* ── Plotly chart background fix ── */
.js-plotly-plot .plotly .svg-container { background: transparent !important; }

/* ── Streamlit widget overrides ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background: var(--bg-overlay) !important;
    border-color: var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
}
[data-testid="stSlider"] [data-testid="stTickBar"] { color: var(--text-muted) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ── Metric (native st.metric override) ── */
[data-testid="metric-container"] {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.2rem 1.4rem !important;
}
[data-testid="stMetricLabel"]  { color: var(--text-secondary) !important; font-size: 0.8rem !important; }
[data-testid="stMetricValue"]  { color: var(--text-primary) !important; }
[data-testid="stMetricDelta"]  { font-size: 0.82rem !important; }

/* ── Sidebar nav item ── */
.nav-item {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.55rem 0.9rem;
    border-radius: var(--radius-sm);
    color: var(--text-secondary);
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    margin-bottom: 2px;
    text-decoration: none;
    transition: background 0.15s, color 0.15s;
}
.nav-item:hover  { background: var(--bg-overlay); color: var(--text-primary); }
.nav-item.active { background: rgba(79,142,247,0.12); color: var(--accent-blue); }
.nav-icon { font-size: 0.95rem; width: 1.1rem; text-align: center; }
.nav-section {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--text-muted);
    padding: 1rem 0.9rem 0.35rem;
}

/* ── Alert / insight box ── */
.insight-box {
    border-radius: var(--radius-md);
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    font-size: 0.875rem;
    border-left: 3px solid;
}
.insight-box.warn  { background: rgba(245,166,35,0.08);  border-color: var(--accent-amber); }
.insight-box.good  { background: rgba(76,175,125,0.08);  border-color: var(--accent-green); }
.insight-box.bad   { background: rgba(240,98,146,0.08);  border-color: var(--accent-rose); }
.insight-box.info  { background: rgba(79,142,247,0.08);  border-color: var(--accent-blue); }

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 5rem 2rem;
    color: var(--text-muted);
}
.empty-icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.3; }

/* ── Score bar ── */
.score-bar-wrap { background: var(--bg-overlay); border-radius: 100px; height: 6px; overflow: hidden; }
.score-bar-fill { height: 6px; border-radius: 100px; background: var(--gradient-hero); }

/* ── Tag row ── */
.tag-row { display: flex; flex-wrap: wrap; gap: 0.4rem; }

/* ── Heatmap cell override ── */
.heatmap-label { font-size: 0.72rem; color: var(--text-secondary); }
</style>
"""


def inject_global_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ── Sidebar renderer ──────────────────────────────────────────────────────────
NAV_ITEMS = [
    ("OVERVIEW", [
        ("◈", "Executive Dashboard", "pages/1_Executive_Dashboard"),
    ]),
    ("INTELLIGENCE", [
        ("▤", "Store Intelligence",   "pages/2_Store_Intelligence"),
        ("◑", "Product Intelligence", "pages/3_Product_Intelligence"),
        ("⊞", "Size Intelligence",    "pages/4_Size_Intelligence"),
        ("◐", "Color Intelligence",   "pages/5_Color_Intelligence"),
        ("▥", "Inventory Intelligence","pages/6_Inventory_Intelligence"),
    ]),
    ("ANALYTICS", [
        ("◎", "Geographic Analytics", "pages/7_Geographic_Analytics"),
        ("◷", "Season & Fit",         "pages/8_Season_Fit_Analytics"),
    ]),
    ("AI", [
        ("✦", "AI Recommendations",   "pages/9_AI_Recommendation_Center"),
    ]),
]


def render_sidebar():
    pass