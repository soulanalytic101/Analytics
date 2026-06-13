"""
components/charts.py — Plotly chart factory with unified dark theme
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# ── Design tokens (mirror CSS vars) ──────────────────────────────────────────
BG        = "rgba(0,0,0,0)"
SURFACE   = "#181b23"
GRIDCOLOR = "rgba(255,255,255,0.05)"
TEXTCOLOR = "#8b90a4"
TICKCOLOR = "#4e5268"

PALETTE = [
    "#4f8ef7", "#9b74f5", "#2ec4b6", "#f5a623",
    "#f06292", "#4caf7d", "#fb8c00", "#80deea",
    "#ce93d8", "#a5d6a7",
]

ACCENT_BLUE   = "#4f8ef7"
ACCENT_VIOLET = "#9b74f5"
ACCENT_TEAL   = "#2ec4b6"
ACCENT_AMBER  = "#f5a623"
ACCENT_ROSE   = "#f06292"
ACCENT_GREEN  = "#4caf7d"


def _base_layout(**kwargs) -> dict:
    return dict(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(family="DM Sans, sans-serif", color=TEXTCOLOR, size=12),
        margin=dict(l=10, r=10, t=36, b=10),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor=GRIDCOLOR,
            font=dict(size=11),
        ),
        xaxis=dict(gridcolor=GRIDCOLOR, tickcolor=TICKCOLOR, linecolor=GRIDCOLOR,
                   tickfont=dict(size=11)),
        yaxis=dict(gridcolor=GRIDCOLOR, tickcolor=TICKCOLOR, linecolor=GRIDCOLOR,
                   tickfont=dict(size=11)),
        colorway=PALETTE,
        **kwargs,
    )


def bar_chart(
    df: pd.DataFrame, x: str, y: str,
    title: str = "", color: str = ACCENT_BLUE,
    orientation: str = "v", height: int = 360,
    text_col: str = None,
) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=df[x] if orientation == "v" else df[y],
        y=df[y] if orientation == "v" else df[x],
        orientation=orientation,
        marker=dict(
            color=color,
            opacity=0.85,
            line=dict(width=0),
        ),
        text=df[text_col] if text_col else None,
        textfont=dict(size=10, color=TEXTCOLOR),
        textposition="outside",
        hovertemplate=f"<b>%{{{'x' if orientation=='v' else 'y'}}}</b><br>{y}: %{{{'y' if orientation=='v' else 'x'}:,.0f}}<extra></extra>",
    ))
    layout = _base_layout(title=dict(text=title, font=dict(size=13, color="#f0f2f8"), x=0))
    layout["height"] = height
    if orientation == "h":
        layout["xaxis"]["showgrid"] = True
        layout["yaxis"]["showgrid"] = False
        layout["yaxis"]["autorange"] = "reversed"
    fig.update_layout(**layout)
    return fig


def grouped_bar(
    df: pd.DataFrame, x: str, y_cols: list[str],
    title: str = "", height: int = 360,
) -> go.Figure:
    fig = go.Figure()
    for i, col in enumerate(y_cols):
        fig.add_trace(go.Bar(
            name=col,
            x=df[x], y=df[col],
            marker_color=PALETTE[i % len(PALETTE)],
            opacity=0.85,
        ))
    fig.update_layout(barmode="group", **_base_layout(
        title=dict(text=title, font=dict(size=13, color="#f0f2f8"), x=0),
        height=height,
    ))
    return fig


def line_chart(
    df: pd.DataFrame, x: str, y_cols: list[str],
    title: str = "", height: int = 300,
) -> go.Figure:
    fig = go.Figure()
    for i, col in enumerate(y_cols):
        fig.add_trace(go.Scatter(
            x=df[x], y=df[col],
            mode="lines",
            name=col,
            line=dict(color=PALETTE[i % len(PALETTE)], width=2.5, shape="spline"),
            fill="tozeroy",
            fillcolor=f"rgba({_hex_to_rgb(PALETTE[i % len(PALETTE)])},0.06)",
        ))
    fig.update_layout(**_base_layout(
        title=dict(text=title, font=dict(size=13, color="#f0f2f8"), x=0),
        height=height,
    ))
    return fig


def area_line(
    df: pd.DataFrame, x: str, y: str,
    title: str = "", color: str = ACCENT_BLUE, height: int = 260,
) -> go.Figure:
    r, g, b = _hex_to_rgb(color)
    fig = go.Figure(go.Scatter(
        x=df[x], y=df[y],
        mode="lines",
        line=dict(color=color, width=2.5, shape="spline"),
        fill="tozeroy",
        fillcolor=f"rgba({r},{g},{b},0.08)",
    ))
    fig.update_layout(**_base_layout(
        title=dict(text=title, font=dict(size=13, color="#f0f2f8"), x=0),
        height=height,
    ))
    return fig


def donut_chart(
    df: pd.DataFrame, names: str, values: str,
    title: str = "", height: int = 320,
) -> go.Figure:
    fig = go.Figure(go.Pie(
        labels=df[names], values=df[values],
        hole=0.62,
        marker=dict(colors=PALETTE, line=dict(color=SURFACE, width=2)),
        textinfo="percent",
        textfont=dict(size=11),
        hovertemplate="<b>%{label}</b><br>%{value:,.0f}<br>%{percent}<extra></extra>",
    ))
    fig.update_layout(**_base_layout(
        title=dict(text=title, font=dict(size=13, color="#f0f2f8"), x=0),
        height=height,
        showlegend=True,
    ))
    return fig


def treemap(
    df: pd.DataFrame, path_cols: list[str], values: str,
    title: str = "", height: int = 420,
) -> go.Figure:
    fig = px.treemap(
        df, path=path_cols, values=values,
        color=values,
        color_continuous_scale=[[0, "#1e2230"], [0.5, "#4f8ef7"], [1.0, "#9b74f5"]],
    )
    fig.update_traces(
        textfont=dict(family="DM Sans", size=12, color="white"),
        marker=dict(line=dict(width=1, color=SURFACE)),
    )
    fig.update_layout(**_base_layout(
        title=dict(text=title, font=dict(size=13, color="#f0f2f8"), x=0),
        height=height,
    ))
    return fig


def heatmap(
    matrix: pd.DataFrame,
    title: str = "", height: int = 400,
    colorscale=None,
) -> go.Figure:
    if colorscale is None:
        colorscale = [[0, "#1e2230"], [0.5, "#4f8ef7"], [1.0, "#9b74f5"]]
    fig = go.Figure(go.Heatmap(
        z=matrix.values,
        x=matrix.columns.tolist(),
        y=matrix.index.tolist(),
        colorscale=colorscale,
        showscale=True,
        hovertemplate="Row: %{y}<br>Col: %{x}<br>Value: %{z:,.0f}<extra></extra>",
    ))
    fig.update_layout(**_base_layout(
        title=dict(text=title, font=dict(size=13, color="#f0f2f8"), x=0),
        height=height,
    ))
    return fig


def scatter_plot(
    df: pd.DataFrame, x: str, y: str,
    size: str = None, color: str = None,
    title: str = "", height: int = 380,
    hover_name: str = None,
) -> go.Figure:
    kwargs = dict(
        data_frame=df, x=x, y=y,
        hover_name=hover_name,
        color_discrete_sequence=PALETTE,
    )
    if size and size in df.columns:
        kwargs["size"] = size
        kwargs["size_max"] = 30
    if color and color in df.columns:
        kwargs["color"] = color

    fig = px.scatter(**kwargs)
    fig.update_traces(marker=dict(opacity=0.75, line=dict(width=0)))
    fig.update_layout(**_base_layout(
        title=dict(text=title, font=dict(size=13, color="#f0f2f8"), x=0),
        height=height,
    ))
    return fig


def bullet_chart(
    df: pd.DataFrame, category_col: str, value_col: str,
    title: str = "", height: int = 360,
) -> go.Figure:
    """Horizontal bar chart styled as a ranking / bullet chart."""
    df_s = df.nlargest(15, value_col).sort_values(value_col)
    fig = go.Figure(go.Bar(
        x=df_s[value_col],
        y=df_s[category_col],
        orientation="h",
        marker=dict(
            color=df_s[value_col],
            colorscale=[[0, "#1e2230"], [0.5, "#4f8ef7"], [1.0, "#9b74f5"]],
            showscale=False,
        ),
    ))
    fig.update_layout(**_base_layout(
        title=dict(text=title, font=dict(size=13, color="#f0f2f8"), x=0),
        height=height,
    ))
    return fig


def funnel_chart(
    df: pd.DataFrame, y: str, x: str,
    title: str = "", height: int = 340,
) -> go.Figure:
    fig = go.Figure(go.Funnel(
        y=df[y], x=df[x],
        marker=dict(color=PALETTE[:len(df)]),
        textinfo="value+percent initial",
    ))
    fig.update_layout(**_base_layout(
        title=dict(text=title, font=dict(size=13, color="#f0f2f8"), x=0),
        height=height,
    ))
    return fig


# ── Utilities ─────────────────────────────────────────────────────────────────
def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def fmt_inr(value: float) -> str:
    """Format as Indian Rupees abbreviated."""
    if value >= 1e7:
        return f"₹{value/1e7:.2f} Cr"
    elif value >= 1e5:
        return f"₹{value/1e5:.1f} L"
    elif value >= 1e3:
        return f"₹{value/1e3:.0f} K"
    return f"₹{value:,.0f}"


def fmt_units(value: float) -> str:
    if value >= 1e6:
        return f"{value/1e6:.2f}M"
    elif value >= 1e3:
        return f"{value/1e3:.1f}K"
    return f"{value:,.0f}"