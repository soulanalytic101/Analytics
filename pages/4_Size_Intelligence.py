import streamlit as st

from analytics.size import (
    best_sizes,
    dead_sizes,
    size_heatmap
)

from components.filters import (
    require_data,
    sidebar_filters
)

from components.charts import (
    bar_chart,
    heatmap
)

df = require_data()

if df is None:
    st.stop()

df = sidebar_filters(
    df,
    include_category=True
)

st.markdown(
    '<div class="page-header">Size </div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-sub">Demand, inventory and reorder insights by size</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    top_sizes = best_sizes(df)

    st.plotly_chart(
        bar_chart(
            top_sizes.head(15),
            "SIZE",
            "units",
            title="Best Selling Sizes"
        ),
        use_container_width=True
    )

with col2:

    dead = dead_sizes(df)

    st.plotly_chart(
        bar_chart(
            dead.head(15),
            "SIZE",
            "inventory",
            title="Dead Sizes"
        ),
        use_container_width=True
    )

st.divider()

import plotly.express as px

size_cat = (
    df.groupby(["CATEGORY", "SIZE"])["QTY SALE"]
    .sum()
    .reset_index()
)

fig = px.bar(
    size_cat,
    x="CATEGORY",
    y="QTY SALE",
    color="SIZE",
    barmode="stack",
    title="Size Demand by Category"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Size Performance Table")

st.dataframe(
    top_sizes,
    use_container_width=True
)