"""
components/kpi_cards.py — Reusable KPI card renderers
"""

import streamlit as st


def kpi_card(label: str, value: str, delta: str = "", delta_positive: bool = True, icon: str = ""):
    """Render a single styled KPI card."""
    delta_class = "up" if delta_positive else "down"
    delta_arrow = "↑" if delta_positive else "↓"
    delta_html = f'<div class="kpi-delta {delta_class}">{delta_arrow} {delta}</div>' if delta else ""
    icon_html   = f'<div class="kpi-icon">{icon}</div>' if icon else ""

    st.markdown(f"""
    <div class="kpi-card">
        {icon_html}
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_kpi_row(metrics: list[dict]):
    """
    metrics: list of dicts with keys: label, value, delta (opt), positive (opt), icon (opt)
    Renders in N equal columns.
    """
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            kpi_card(
                label=m["label"],
                value=m["value"],
                delta=m.get("delta", ""),
                delta_positive=m.get("positive", True),
                icon=m.get("icon", ""),
            )


def insight_box(text: str, kind: str = "info"):
    """kind: info | good | warn | bad"""
    icons = {"info": "ℹ", "good": "✓", "warn": "⚠", "bad": "✕"}
    st.markdown(f"""
    <div class="insight-box {kind}">
        <strong>{icons.get(kind,'')}</strong>&nbsp; {text}
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str, subtitle: str = ""):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p style="color:var(--text-muted);font-size:0.8rem;margin-top:-0.5rem">{subtitle}</p>',
                    unsafe_allow_html=True)


def badge(text: str, color: str = "blue") -> str:
    return f'<span class="badge badge-{color}">{text}</span>'


def score_bar(score: float, max_score: float = 100) -> str:
    pct = min(score / max_score * 100, 100)
    return f"""
    <div class="score-bar-wrap">
        <div class="score-bar-fill" style="width:{pct:.1f}%"></div>
    </div>
    """