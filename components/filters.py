"""
components/filters.py — Shared sidebar filter widget factory
"""

import streamlit as st
import pandas as pd


def require_data():

    if "df" not in st.session_state:
        st.warning(
            "Upload a dataset from the Dashboard page first."
        )
        return None

    return st.session_state["df"]


def sidebar_filters(
    df: pd.DataFrame,
    include_zone:     bool = True,
    include_state:    bool = True,
    include_city:     bool = False,
    include_store:    bool = False,
    include_brand:    bool = False,
    include_category: bool = False,
    include_season:   bool = False,
    include_month:    bool = True,
) -> pd.DataFrame:
    """
    Render sidebar filters and return filtered DataFrame.
    All filters are additive.
    """
    filtered = df.copy()

    with st.sidebar:
        st.markdown('<div class="nav-section">FILTERS</div>', unsafe_allow_html=True)

        if include_month and "_MONTH" in df.columns:
            months = sorted(df["_MONTH"].dropna().unique())
            sel_months = st.multiselect("Month", months, default=[], key="filter_month")
            if sel_months:
                filtered = filtered[filtered["_MONTH"].isin(sel_months)]

        if include_zone and "ZONE" in df.columns:
            zones = sorted(df["ZONE"].dropna().unique())
            sel_zones = st.multiselect("Zone", zones, default=[], key="filter_zone")
            if sel_zones:
                filtered = filtered[filtered["ZONE"].isin(sel_zones)]

        if include_state and "STATE" in df.columns:
            states = sorted(df["STATE"].dropna().unique())
            sel_states = st.multiselect("State", states, default=[], key="filter_state")
            if sel_states:
                filtered = filtered[filtered["STATE"].isin(sel_states)]

        if include_city and "CITY" in df.columns:
            cities = sorted(df["CITY"].dropna().unique())
            sel_cities = st.multiselect("City", cities, default=[], key="filter_city")
            if sel_cities:
                filtered = filtered[filtered["CITY"].isin(sel_cities)]

        if include_store and "NAME" in df.columns:
            stores = sorted(df["NAME"].dropna().unique())
            sel_stores = st.multiselect("Store", stores, default=[], key="filter_store")
            if sel_stores:
                filtered = filtered[filtered["NAME"].isin(sel_stores)]

        if include_brand and "BRAND" in df.columns:
            brands = sorted(df["BRAND"].dropna().unique())
            sel_brands = st.multiselect("Brand", brands, default=[], key="filter_brand")
            if sel_brands:
                filtered = filtered[filtered["BRAND"].isin(sel_brands)]

        if include_category and "MAIN CATEGORY" in df.columns:
            cats = sorted(df["MAIN CATEGORY"].dropna().unique())
            sel_cats = st.multiselect("Category", cats, default=[], key="filter_cat")
            if sel_cats:
                filtered = filtered[filtered["MAIN CATEGORY"].isin(sel_cats)]

        if include_season and "SEASON" in df.columns:
            seasons = sorted(df["SEASON"].dropna().unique())
            sel_seasons = st.multiselect("Season", seasons, default=[], key="filter_season")
            if sel_seasons:
                filtered = filtered[filtered["SEASON"].isin(sel_seasons)]

        # Row count indicator
        n_orig = len(df)
        n_filt = len(filtered)
        pct    = n_filt / n_orig * 100 if n_orig else 0
        st.markdown(f"""
        <div style="font-size:0.72rem;color:#4e5268;padding:0.6rem 0.9rem 0;border-top:1px solid var(--border);margin-top:0.5rem">
            Showing <span style="color:#f0f2f8;font-weight:600">{n_filt:,}</span>
            of {n_orig:,} rows ({pct:.0f}%)
        </div>
        """, unsafe_allow_html=True)

    return filtered