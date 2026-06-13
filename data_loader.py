import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
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

    uploaded_file = st.file_uploader(
        "Upload Sales Dataset",
        type=["csv"]
    )

    if uploaded_file is None:
        return None

    df = pd.read_csv(
        uploaded_file,
        low_memory=False
    )

    return process_data(df)