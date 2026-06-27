import streamlit as st

from analytics.color import (
    top_colors,
    weak_colors,
    color_by_state
)

from components.filters import (
    require_data,
    sidebar_filters
)

from components.charts import (
    bar_chart
)

from db import load_granular_data

selected_brand = st.session_state.get("selected_brand", "Killer")
cols = ["SHADE", "STATE", "NET SALE VALUE", "QTY SALE", "CLSNG QTY", "MAIN CATEGORY", "CATEGORY"]
df = load_granular_data(selected_brand, cols)

if df is None or df.empty:
    st.stop()

df = sidebar_filters(
    df,
    include_state=True,
    include_category=True
)

st.markdown(
    '<div class="page-header">Color </div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-sub">Color performance and demand insights</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    colors = top_colors(df)

    st.plotly_chart(
        bar_chart(
            colors.head(15),
            "SHADE",
            "revenue",
            title="Top Colors"
        ),
        use_container_width=True
    )

with col2:

    weak = weak_colors(df)

    st.plotly_chart(
        bar_chart(
            weak.head(15),
            "SHADE",
            "revenue",
            title="Weak Colors"
        ),
        use_container_width=True
    )

st.divider()

state_color = color_by_state(df)

st.subheader("Color Performance by State")

st.dataframe(
    state_color.sort_values(
        "NET SALE VALUE",
        ascending=False
    ),
    use_container_width=True
)