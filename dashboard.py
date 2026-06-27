import streamlit as st
from auth import require_login
from data_loader import load_data
from db import load_store_performance

from components.sidebar import (
    inject_global_css,
    render_sidebar
)

from components.filters import sidebar_filters
from components.kpi_cards import render_kpi_row
from components.charts import bar_chart, area_line



# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="RetailIQ",
    
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------

inject_global_css()
require_login()

# --------------------------------------------------
df_new = load_data()

if df_new is not None:
    st.session_state["df"] = df_new

# We do not use st.stop() immediately. We will check if "df" is in session state
# and display info, but we still allow the dashboard controls/loaders to run.
df = st.session_state.get("df", None)

if df is None:
    st.info("Upload a sales dataset to begin.")
else:
    # --------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------

    render_sidebar()

    # --------------------------------------------------
    # FILTERS
    # --------------------------------------------------

    df = sidebar_filters(df)
    if "BRAND_GROUP" in df.columns:

        selected_brand = st.sidebar.selectbox(
            "Brand",
            [
                "All Brands",
                "Killer",
                "JR Killer",
                "Pepe"
            ]
        )

        if selected_brand != "All Brands":

            df = df[
                df["BRAND_GROUP"] == selected_brand
            ]
    col_logo, col_title = st.columns([1, 8])



    with col_title:
        st.markdown(
            '<h1 class="hero-title">RetailIQ</h1>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<p class="hero-sub">INTELLIGENCE SUITE</p>',
            unsafe_allow_html=True
        )

    st.divider()

    # --------------------------------------------------
    # EXECUTIVE DASHBOARD
    # --------------------------------------------------

    st.markdown(
        '<div class="page-header">Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-sub">Enterprise overview of retail performance</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # KPIs
    # --------------------------------------------------

    revenue = df["NET SALE VALUE"].sum()
    units = df["QTY SALE"].sum()
    discount = df["DISCOUNT VALUE"].sum()

    render_kpi_row([
        {
            "label": "Revenue",
            "value": f"₹{revenue:,.0f}",
            "icon": "₹"
        },
        {
            "label": "Units Sold",
            "value": f"{units:,.0f}",
            "icon": "📦"
        },
        {
            "label": "Discount Given",
            "value": f"₹{discount:,.0f}",
            "icon": "%"
        }
    ])

    st.divider()

    # --------------------------------------------------
    # MONTHLY TREND
    # --------------------------------------------------

    if "_MONTH" in df.columns:

        monthly = (
            df.groupby("_MONTH")["NET SALE VALUE"]
            .sum()
            .reset_index()
            .sort_values("_MONTH")
        )

        st.plotly_chart(
            area_line(
                monthly,
                "_MONTH",
                "NET SALE VALUE",
                title="Monthly Revenue Trend"
            ),
            use_container_width=True
        )

    # --------------------------------------------------
    # TOP CATEGORIES + STORES
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        categories = (
            df.groupby("MAIN CATEGORY")
            ["NET SALE VALUE"]
            .sum()
            .reset_index()
            .sort_values(
                "NET SALE VALUE",
                ascending=False
            )
            .head(10)
        )

        st.plotly_chart(
            bar_chart(
                categories,
                "MAIN CATEGORY",
                "NET SALE VALUE",
                title="Top Categories"
            ),
            use_container_width=True
        )

    with col2:
        # Load and filter store performance from db view
        stores_raw = load_store_performance(st.session_state.get("selected_brand", "Killer"))
        if not stores_raw.empty:
            if st.session_state.get("filter_zone"):
                stores_raw = stores_raw[stores_raw["ZONE"].isin(st.session_state["filter_zone"])]
            if st.session_state.get("filter_state"):
                stores_raw = stores_raw[stores_raw["STATE"].isin(st.session_state["filter_state"])]
            if st.session_state.get("filter_city"):
                stores_raw = stores_raw[stores_raw["CITY"].isin(st.session_state["filter_city"])]
            
            stores = (
                stores_raw.groupby("NAME")["NET SALE VALUE"]
                .sum()
                .reset_index()
                .sort_values("NET SALE VALUE", ascending=False)
                .head(10)
            )
        else:
            stores = pd.DataFrame(columns=["NAME", "NET SALE VALUE"])

        st.plotly_chart(
            bar_chart(
                stores,
                "NAME",
                "NET SALE VALUE",
                title="Top Stores"
            ),
            use_container_width=True
        )

        st.write("Rows loaded into dashboard:", len(df))