import pandas as pd
import streamlit as st


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
        df["_YEAR"] = df["INVOICE DATE"].dt.year
        df["_MONTH"] = (
            df["INVOICE DATE"]
            .dt.to_period("M")
            .astype(str)
        )

    return df


def load_data():

    st.subheader("Upload Brand Files")

    killer_files = st.file_uploader(
        "Killer",
        type=["xlsx"],
        accept_multiple_files=True,
        key="killer"
    )

    jrkiller_files = st.file_uploader(
        "JR Killer",
        type=["xlsx"],
        accept_multiple_files=True,
        key="jrkiller"
    )

    pepe_files = st.file_uploader(
        "Pepe",
        type=["xlsx"],
        accept_multiple_files=True,
        key="pepe"
    )

    dfs = []

    brand_uploads = [
        ("Killer", killer_files),
        ("JR Killer", jrkiller_files),
        ("Pepe", pepe_files)
    ]

    with st.spinner("Loading datasets..."):

        for brand_name, files in brand_uploads:

            if not files:
                continue

            for file in files:

                temp_df = pd.read_excel(
                    file,
                    engine="openpyxl"
                )

                temp_df["BRAND_GROUP"] = brand_name

                dfs.append(temp_df)

    if not dfs:
        return None

    df = pd.concat(
        dfs,
        ignore_index=True
    )

    st.sidebar.markdown("### Loaded Files")

    for brand_name, files in brand_uploads:

        if files:

            st.sidebar.markdown(f"**{brand_name}**")

            for file in files:
                st.sidebar.write(f"• {file.name}")

    return process_data(df)