import streamlit as st

from analytics.recommendations import (
    generate_recommendations
)

from components.filters import (
    require_data,
    sidebar_filters
)

from components.kpi_cards import (
    insight_box
)

df = require_data()

if df is None:
    st.stop()

df = sidebar_filters(df)

st.markdown(
    '<div class="page-header">AI Recommendation </div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-sub">Automatically generated retail intelligence insights</div>',
    unsafe_allow_html=True
)

recommendations = generate_recommendations(df)

st.subheader("Recommendations")

for rec in recommendations:

    insight_box(
        rec,
        kind="good"
    )

st.divider()

st.subheader("Inventory Opportunities")

dead_stock = len(
    df[
        (df["CLSNG QTY"] > 20)
        &
        (df["QTY SALE"] == 0)
    ]
)

insight_box(
    f"{dead_stock:,} records are potential dead stock.",
    kind="warn"
)

st.subheader("Store Intelligence")

top_store = (
    df.groupby("NAME")
    ["NET SALE VALUE"]
    .sum()
    .idxmax()
)

insight_box(
    f"{top_store} is currently the highest revenue generating store.",
    kind="good"
)

st.subheader("Color Intelligence")

top_color = (
    df.groupby("SHADE")
    ["NET SALE VALUE"]
    .sum()
    .idxmax()
)

insight_box(
    f"{top_color} is the highest performing color across the network.",
    kind="info"
)

st.subheader("Size Intelligence")

top_size = (
    df.groupby("SIZE")
    ["QTY SALE"]
    .sum()
    .idxmax()
)

insight_box(
    f"Increase stock allocation for Size {top_size}.",
    kind="good"
)