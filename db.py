import os
import numpy as np
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

COL_MAP = {
    "SR.NO": "sr_no",
    "INVOICE DATE": "invoice_date",
    "NEW DATE": "new_date",
    "MONTH": "month",
    "BILL NO INVOICE NO": "bill_no",
    "NAME AS PER REPORT RECEIVED": "store_name_report",
    "NAME": "name",
    "STORE CODE": "store_code",
    "BRAND": "brand",
    "REPORT STATUS": "report_status",
    "STORE STATUS": "store_status",
    "TYPE": "type",
    "ZONE": "zone",
    "CITY": "city",
    "STATE": "state",
    "DISTRIBUTOR NAME": "distributor_name",
    "ASM / RSM": "asm_rsm",
    "EAN CODE": "ean_code",
    "NEW EAN CODE": "new_ean_code",
    "MAIN CATEGORY": "main_category",
    "ITEM NAME": "item_name",
    "CATEGORY": "category",
    "SHADE": "shade",
    "SIZE": "size",
    "SEASON": "season",
    "MRP": "mrp",
    "FIT": "fit",
    "PRINT TYPE": "print_type",
    "CLSNG QTY": "clsng_qty",
    "CLSNG VALUE": "clsng_value",
    "QTY SALE": "qty_sale",
    "NET SALE VALUE": "net_sale_value",
    "DISCOUNT VALUE": "discount_value",
    "MRP SALE VALUE": "mrp_sale_value",
    "% Sale": "pct_sale"
}

REVERSE_COL_MAP = {
    v: k
    for k, v in COL_MAP.items()
}


def get_brands() -> list[str]:

    result = (
        supabase
        .table("sales_data")
        .select("brand")
        .execute()
    )

    brands = list(
        {
            row["brand"]
            for row in result.data
        }
    )

    return sorted(brands)


def load_brand_data(
    brand: str
) -> pd.DataFrame:

    all_rows = []

    CHUNK_SIZE = 10000
    start = 0

    while True:

        result = (
            supabase
            .table("sales_data")
            .select("*")
            .eq("brand", brand)
            .range(
                start,
                start + CHUNK_SIZE - 1
            )
            .execute()
        )

        rows = result.data
        print("Fetched:", len(rows))

        if not rows:
            break

        all_rows.extend(rows)

        start += CHUNK_SIZE

        print(
            f"Loaded {len(all_rows):,} rows..."
        )

    if not all_rows:
        return pd.DataFrame()

    df = pd.DataFrame(all_rows)

    df = df.drop(
        columns=["id"],
        errors="ignore"
    )

    df = df.rename(
        columns=REVERSE_COL_MAP
    )

    return df


def upload_and_append(
    df: pd.DataFrame,
    brand: str
) -> dict:

    import streamlit as st

    df = df.copy()

    df["BRAND"] = brand

    df = df.rename(
        columns=COL_MAP
    )

    valid_cols = list(
        COL_MAP.values()
    )

    df = df[
        [
            c
            for c in valid_cols
            if c in df.columns
        ]
    ]

    for col in [
        "invoice_date",
        "new_date"
    ]:

        if col in df.columns:

            df[col] = (
                pd.to_datetime(
                    df[col],
                    errors="coerce"
                )
                .dt.strftime("%Y-%m-%d")
            )

    df = df.astype(object)

    df = df.replace(
        [np.nan, np.inf, -np.inf],
        None
    )

    rows = df.to_dict(
        orient="records"
    )

    CHUNK_SIZE = 6000

    inserted = 0

    progress_bar = st.progress(0)

    for i in range(
        0,
        len(rows),
        CHUNK_SIZE
    ):

        chunk = rows[
            i:i + CHUNK_SIZE
        ]

        try:

            result = (
                supabase
                .table("sales_data")
                .upsert(
                    chunk,
                    on_conflict="brand,bill_no,ean_code",
                    ignore_duplicates=True
                )
                .execute()
            )

            if result.data:
                inserted += len(
                    result.data
                )

            progress_bar.progress(
                min(
                    i + CHUNK_SIZE,
                    len(rows)
                ) / len(rows)
            )

        except Exception as e:

            print(
                f"Chunk failed at row {i}"
            )

            print(str(e))

            raise

    progress_bar.empty()

    skipped = (
        len(rows) - inserted
    )

    return {
        "inserted": inserted,
        "skipped": skipped
    }