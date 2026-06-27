import streamlit as st
import pandas as pd

from components.filters import (
    require_data,
    sidebar_filters
)

from components.charts import (
    bar_chart
)

from db import load_granular_data

selected_brand = st.session_state.get("selected_brand", "Killer")
cols = ["SEASON", "FIT", "PRINT TYPE", "NET SALE VALUE", "QTY SALE", "MAIN CATEGORY", "ZONE", "STATE", "CITY"]
df = load_granular_data(selected_brand, cols)

if df is None or df.empty:
    st.stop()

df = sidebar_filters(
    df,
    include_season=True,
    include_category=True
)

st.markdown(
    '<div class="page-header">Season & Fit Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-sub">Seasonal demand and fit preference intelligence</div>',
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(
    [
        "Season",
        "Fit",
        "Print Type"
    ]
)

with tab1:

    season = (
        df.groupby("SEASON")
        ["NET SALE VALUE"]
        .sum()
        .reset_index()
        .sort_values(
            "NET SALE VALUE",
            ascending=False
        )
    )

    st.plotly_chart(
        bar_chart(
            season,
            "SEASON",
            "NET SALE VALUE",
            title="Revenue By Season"
        ),
        use_container_width=True
    )

    st.dataframe(
        season,
        use_container_width=True
    )

with tab2:

    fit = (
        df.groupby("FIT")
        ["NET SALE VALUE"]
        .sum()
        .reset_index()
        .sort_values(
            "NET SALE VALUE",
            ascending=False
        )
    )

    st.plotly_chart(
        bar_chart(
            fit,
            "FIT",
            "NET SALE VALUE",
            title="Revenue By Fit"
        ),
        use_container_width=True
    )

    st.dataframe(
        fit,
        use_container_width=True
    )

with tab3:

    prints = (
        df.groupby("PRINT TYPE")
        ["NET SALE VALUE"]
        .sum()
        .reset_index()
        .sort_values(
            "NET SALE VALUE",
            ascending=False
        )
    )

    st.plotly_chart(
        bar_chart(
            prints,
            "PRINT TYPE",
            "NET SALE VALUE",
            title="Revenue By Print Type"
        ),
        use_container_width=True
    )

    st.dataframe(
        prints,
        use_container_width=True
    )