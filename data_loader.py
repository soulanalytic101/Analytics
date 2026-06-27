import pandas as pd
import streamlit as st

from db import (
    load_brand_data,
    upload_and_append,
    load_monthly_sales
)


@st.cache_data(show_spinner=True)
def process_data(df):
    if df is None or df.empty:
        return df

    df = df.copy()

    df.columns = (
        df.columns
        .str.replace("\n", " ", regex=False)
        .str.replace("  ", " ", regex=False)
        .str.strip()
    )

    for col in ["INVOICE DATE", "NEW DATE"]:
        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col],
                errors="coerce",
                dayfirst=True
            )

    numeric_cols = [
        "MRP",
        "CLSNG QTY",
        "CLSNG VALUE",
        "QTY SALE",
        "NET SALE VALUE",
        "DISCOUNT VALUE",
        "MRP SALE VALUE",
        "% Sale"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    if "INVOICE DATE" in df.columns:

        df["_YEAR"] = (
            df["INVOICE DATE"]
            .dt.year
        )

        df["_MONTH"] = (
            df["INVOICE DATE"]
            .dt.to_period("M")
            .astype(str)
        )

    # Downcast numerics to save memory
    for col in df.select_dtypes(include=["float"]).columns:
        df[col] = pd.to_numeric(df[col], downcast="float")
    for col in df.select_dtypes(include=["integer"]).columns:
        df[col] = pd.to_numeric(df[col], downcast="integer")

    # Convert low-cardinality string columns to category dtype
    categorical_cols = ["ZONE", "STATE", "CITY", "MAIN CATEGORY", "SEASON", "SIZE", "FIT", "BRAND", "CATEGORY"]
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")

    return df


@st.cache_data(show_spinner=True)
def cached_load_brand_data(brand: str):
    return load_brand_data(brand)


def load_data():

    st.subheader("Brand Data Management")

    with st.expander(
        "Upload Brand Files",
        expanded=True
    ):

        col1, col2, col3 = st.columns(3)

        # -----------------------------
        # KILLER
        # -----------------------------

        with col1:

            killer_files = st.file_uploader(
                "Killer",
                type=["xlsx", "xlsb"],
                accept_multiple_files=True,
                key="killer_upload"
            )

            if killer_files:

                for file in killer_files:
                    file_ext = file.name.split(".")[-1].lower()
                    engine = "pyxlsb" if file_ext == "xlsb" else "openpyxl"

                    with st.spinner(f"Reading and parsing {file.name}..."):
                        temp_df = pd.read_excel(
                            file,
                            engine=engine,
                            sheet_name="DATA"
                        )

                    temp_df = process_data(
                        temp_df
                    )

                    stats = upload_and_append(
                        temp_df,
                        "Killer"
                    )

                    st.success(
                        f"{file.name}: "
                        f"{stats['inserted']} inserted, "
                        f"{stats['skipped']} skipped"
                    )

        # -----------------------------
        # JR KILLER
        # -----------------------------

        with col2:

            jrkiller_files = st.file_uploader(
                "JR Killer",
                type=["xlsx", "xlsb"],
                accept_multiple_files=True,
                key="jrkiller_upload"
            )

            if jrkiller_files:

                for file in jrkiller_files:
                    file_ext = file.name.split(".")[-1].lower()
                    engine = "pyxlsb" if file_ext == "xlsb" else "openpyxl"

                    with st.spinner(f"Reading and parsing {file.name}..."):
                        temp_df = pd.read_excel(
                            file,
                            engine=engine,
                            sheet_name="DATA"
                        )

                    temp_df = process_data(
                        temp_df
                    )

                    stats = upload_and_append(
                        temp_df,
                        "JR Killer"
                    )

                    st.success(
                        f"{file.name}: "
                        f"{stats['inserted']} inserted, "
                        f"{stats['skipped']} skipped"
                    )

        # -----------------------------
        # PEPE
        # -----------------------------

        with col3:

            pepe_files = st.file_uploader(
                "Pepe",
                type=["xlsx", "xlsb"],
                accept_multiple_files=True,
                key="pepe_upload"
            )

            if pepe_files:

                for file in pepe_files:
                    file_ext = file.name.split(".")[-1].lower()
                    engine = "pyxlsb" if file_ext == "xlsb" else "openpyxl"

                    with st.spinner(f"Reading and parsing {file.name}..."):
                        temp_df = pd.read_excel(
                            file,
                            engine=engine,
                            sheet_name="DATA"
                        )

                    temp_df = process_data(
                        temp_df
                    )

                    stats = upload_and_append(
                        temp_df,
                        "Pepe"
                    )

                    st.success(
                        f"{file.name}: "
                        f"{stats['inserted']} inserted, "
                        f"{stats['skipped']} skipped"
                    )

    # ---------------------------------
    # BRAND SELECTOR FOR ANALYTICS
    # ---------------------------------

    selected_brand = st.sidebar.selectbox(
        "Brand",
        [
            "Killer",
            "JR Killer",
            "Pepe"
        ]
    )
    st.session_state["selected_brand"] = selected_brand

    df = load_monthly_sales(
        selected_brand
    )

    if df.empty:
        return None

    st.sidebar.success(
        f"Viewing: {selected_brand}"
    )

    return process_data(df)