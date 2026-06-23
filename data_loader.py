import pandas as pd
import streamlit as st

from db import (
    load_brand_data,
    upload_and_append
)


@st.cache_data(show_spinner=True)
def process_data(df):

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

    return df


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
                type=["xlsx"],
                accept_multiple_files=True,
                key="killer_upload"
            )

            if killer_files:

                for file in killer_files:

                    temp_df = pd.read_excel(
                        file,
                        engine="openpyxl"
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
                type=["xlsx"],
                accept_multiple_files=True,
                key="jrkiller_upload"
            )

            if jrkiller_files:

                for file in jrkiller_files:

                    temp_df = pd.read_excel(
                        file,
                        engine="openpyxl"
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
                type=["xlsx"],
                accept_multiple_files=True,
                key="pepe_upload"
            )

            if pepe_files:

                for file in pepe_files:

                    temp_df = pd.read_excel(
                        file,
                        engine="openpyxl"
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

    df = load_brand_data(
        selected_brand
    )

    if df.empty:

        st.warning(
            f"No data available for {selected_brand}"
        )

        return None

    st.sidebar.success(
        f"Viewing: {selected_brand}"
    )

    return process_data(df)