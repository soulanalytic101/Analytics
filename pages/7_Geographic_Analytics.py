import streamlit as st

from analytics.geo import (
    state_performance,
    city_performance,
    zone_performance
)

from components.filters import (
    require_data,
    sidebar_filters
)

from components.charts import (
    bar_chart
)

df = require_data()

if df is None:
    st.stop()

df = sidebar_filters(
    df,
    include_zone=True,
    include_state=True,
    include_city=True,
    include_category=True
)

st.markdown(
    '<div class="page-header">Geographic Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-sub">Regional sales performance across states, cities and zones</div>',
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(
    [
        "State Analysis",
        "City Analysis",
        "Zone Analysis"
    ]
)

with tab1:

    states = state_performance(df)

    st.plotly_chart(
        bar_chart(
            states.head(20),
            "STATE",
            "revenue",
            title="Revenue By State"
        ),
        use_container_width=True
    )

    st.dataframe(
        states,
        use_container_width=True
    )

with tab2:

    cities = city_performance(df)

    st.plotly_chart(
        bar_chart(
            cities.head(20),
            "CITY",
            "revenue",
            title="Revenue By City"
        ),
        use_container_width=True
    )

    st.dataframe(
        cities,
        use_container_width=True
    )

with tab3:

    zones = zone_performance(df)

    st.plotly_chart(
        bar_chart(
            zones,
            "ZONE",
            "revenue",
            title="Revenue By Zone"
        ),
        use_container_width=True
    )

    st.dataframe(
        zones,
        use_container_width=True
    )