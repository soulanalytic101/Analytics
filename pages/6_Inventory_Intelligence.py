import streamlit as st

from analytics.inventory import (
    inventory_summary,
    dead_stock,
    fast_movers,
    slow_movers,
    inventory_health_score
)

from components.filters import (
    require_data,
    sidebar_filters
)

from components.charts import (
    bar_chart
)

from components.kpi_cards import (
    render_kpi_row
)

from db import load_granular_data

selected_brand = st.session_state.get("selected_brand", "Killer")
cols = [
    "MAIN CATEGORY", "ITEM NAME", "CLSNG QTY", "CLSNG VALUE", 
    "QTY SALE", "NET SALE VALUE", "STORE CODE", "NAME", "CITY", "STATE", "ZONE"
]
df = load_granular_data(selected_brand, cols)

if df is None or df.empty:
    st.stop()

df = sidebar_filters(
    df,
    include_category=True,
    include_store=True
)

st.markdown(
    '<div class="page-header">Inventory </div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-sub">Inventory health, stock risk and movement analytics</div>',
    unsafe_allow_html=True
)

health = inventory_health_score(df)

render_kpi_row([
    {
        "label":"Inventory Health",
        "value":f"{health:.1f}%",
        "icon":"📦"
    }
])

summary = inventory_summary(df)

st.plotly_chart(
    bar_chart(
        summary,
        "MAIN CATEGORY",
        "inventory_value",
        title="Inventory Value by Category"
    ),
    use_container_width=True
)

st.divider()

tab1, tab2, tab3 = st.tabs(
    [
        "Dead Stock",
        "Fast Movers",
        "Slow Movers"
    ]
)

with tab1:

    st.dataframe(
        dead_stock(df).head(100),
        use_container_width=True
    )

with tab2:

    st.dataframe(
        fast_movers(df),
        use_container_width=True
    )

with tab3:

    st.dataframe(
        slow_movers(df),
        use_container_width=True
    )