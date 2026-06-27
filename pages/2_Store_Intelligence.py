import streamlit as st

from analytics.store import store_summary
from components.filters import require_data, sidebar_filters
from components.charts import bar_chart

from db import load_granular_data

selected_brand = st.session_state.get("selected_brand", "Killer")
cols = [
    "STORE CODE", "NAME", "CITY", "STATE", "ZONE", 
    "NET SALE VALUE", "QTY SALE", "DISCOUNT VALUE", 
    "MRP SALE VALUE", "BILL NO INVOICE NO", "CLSNG VALUE", "CLSNG QTY"
]
df = load_granular_data(selected_brand, cols)

if df is None or df.empty:
    st.stop()

df = sidebar_filters(
    df,
    include_store=True,
    include_city=True,
    include_category=True
)

st.markdown('<div class="page-header">Store </div>', unsafe_allow_html=True)

stores = store_summary(df)

stores["revenue"] = stores["revenue"].fillna(0).round(0).astype(int)
stores["units"] = stores["units"].fillna(0).round(0).astype(int)
stores["sell_through"] = (
    stores["sell_through"]
    .fillna(0)
    .round(0)
    .astype(int)
    .astype(str) + "%"
)

top10 = stores.head(10)

st.plotly_chart(
    bar_chart(
        top10,
        "NAME",
        "revenue",
        title="Top Stores By Revenue"
    ),
    use_container_width=True
)
st.caption(
    "📌 Sell Through (%) = Units Sold ÷ (Units Sold + Closing Inventory) × 100"
)
st.subheader("Store Performance Leaderboard")

display_df = stores[
    [
        "NAME",
        "CITY",
        "revenue",
        "units",
        "sell_through"
    ]
].copy()

display_df.columns = [
    "Store",
    "City",
    "Revenue (₹)",
    "Units Sold",
    "Sell Through (%)"
]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)