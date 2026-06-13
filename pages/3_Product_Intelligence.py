import streamlit as st

from analytics.product import (
    brand_summary,
    item_ranking
)

from components.filters import require_data, sidebar_filters
from components.charts import bar_chart

df = require_data()

if df is None:
    st.stop()

df = sidebar_filters(
    df,
    include_brand=True,
    include_category=True
)

st.markdown(
    '<div class="page-header">Product Intelligence</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# FIT ANALYTICS
# --------------------------------------------------

fit_sales = (
    df.groupby("FIT")["NET SALE VALUE"]
    .sum()
    .reset_index()
    .sort_values(
        "NET SALE VALUE",
        ascending=False
    )
)

st.plotly_chart(
    bar_chart(
        fit_sales.head(10),
        "FIT",
        "NET SALE VALUE",
        title="Revenue by Fit"
    ),
    use_container_width=True
)

# --------------------------------------------------
# PRINT TYPE ANALYTICS
# --------------------------------------------------

print_sales = (
    df.groupby("PRINT TYPE")["NET SALE VALUE"]
    .sum()
    .reset_index()
    .sort_values(
        "NET SALE VALUE",
        ascending=False
    )
)

st.plotly_chart(
    bar_chart(
        print_sales.head(10),
        "PRINT TYPE",
        "NET SALE VALUE",
        title="Revenue by Print Type"
    ),
    use_container_width=True
)

# --------------------------------------------------
# TOP PRODUCTS
# --------------------------------------------------

st.subheader("Top Products")
st.caption(
    "📌 Unit Share (%) = Units Sold ÷ Total Units Sold × 100"
)

products = item_ranking(df)
total_units = products["units"].sum()

products["unit_share"] = (
    products["units"] / total_units * 100
).round(1)

display_df = products[
    [
        "ITEM NAME",
        "revenue",
        "units",
        "unit_share",
        "stores",
        "avg_mrp"
    ]
].copy()

display_df.columns = [
    "Product",
    "Revenue (₹)",
    "Units Sold",
    "Units Share (%)",
    "Stores Selling",
    "Average MRP (₹)"
]

display_df["Revenue (₹)"] = (
    display_df["Revenue (₹)"]
    .round()
    .astype(int)
)

display_df["Units Sold"] = (
    display_df["Units Sold"]
    .round()
    .astype(int)
)

display_df["Stores Selling"] = (
    display_df["Stores Selling"]
    .astype(int)
)

display_df["Average MRP (₹)"] = (
    display_df["Average MRP (₹)"]
    .round()
    .astype(int)
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)