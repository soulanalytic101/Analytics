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
    "EAN CODE": "new_ean_code",
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


COLS_TO_FETCH = [
    "invoice_date",
    "store_code",
    "name",
    "city",
    "state",
    "zone",
    "net_sale_value",
    "qty_sale",
    "discount_value",
    "mrp_sale_value",
    "clsng_value",
    "clsng_qty",
    "bill_no",
    "main_category",
    "brand",
    "size",
    "shade",
    "season",
    "mrp",
    "fit",
    "item_name",
    "category",
]


def _fetch_all_pages(source: str, brand: str, select_cols: str) -> pd.DataFrame:
    all_rows = []
    CHUNK_SIZE = 1000
    start = 0
    while True:
        try:
            result = (
                supabase
                .table(source)
                .select(select_cols)
                .eq("brand", brand)
                .range(start, start + CHUNK_SIZE - 1)
                .execute()
            )
            rows = result.data
        except Exception as e:
            print(f"Error fetching from {source}: {e}")
            break

        if not rows:
            break

        all_rows.extend(rows)
        if len(rows) < CHUNK_SIZE:
            break
        start += CHUNK_SIZE
    
    return pd.DataFrame(all_rows) if all_rows else pd.DataFrame()


def load_monthly_sales(brand: str) -> pd.DataFrame:
    df = _fetch_all_pages(
        "v_monthly_sales", 
        brand, 
        "brand,f_year,month,f_year_month,zone,state,city,main_category,total_qty,total_net_sales,total_mrp_sales,total_discount"
    )
    if df.empty:
        return df
    
    # Rename to match expected dashboard column names
    rename_map = {
        "f_year": "F_YEAR",
        "month": "MONTH",
        "f_year_month": "_MONTH",
        "zone": "ZONE",
        "state": "STATE",
        "city": "CITY",
        "main_category": "MAIN CATEGORY",
        "total_qty": "QTY SALE",
        "total_net_sales": "NET SALE VALUE",
        "total_mrp_sales": "MRP SALE VALUE",
        "total_discount": "DISCOUNT VALUE",
        "brand": "BRAND"
    }
    return df.rename(columns=rename_map)


def load_store_performance(brand: str) -> pd.DataFrame:
    df = _fetch_all_pages(
        "v_store_performance", 
        brand, 
        "brand,store_code,name,city,state,zone,total_qty,total_net_sales,total_discount"
    )
    if df.empty:
        return df
    
    rename_map = {
        "store_code": "STORE CODE",
        "name": "NAME",
        "city": "CITY",
        "state": "STATE",
        "zone": "ZONE",
        "total_qty": "QTY SALE",
        "total_net_sales": "NET SALE VALUE",
        "total_discount": "DISCOUNT VALUE",
        "brand": "BRAND"
    }
    return df.rename(columns=rename_map)


def load_category_sales(brand: str) -> pd.DataFrame:
    df = _fetch_all_pages(
        "v_category_sales", 
        brand, 
        "brand,f_year,main_category,category,season,total_qty,total_net_sales,total_mrp_sales"
    )
    if df.empty:
        return df
        
    rename_map = {
        "f_year": "F_YEAR",
        "main_category": "MAIN CATEGORY",
        "category": "CATEGORY",
        "season": "SEASON",
        "total_qty": "QTY SALE",
        "total_net_sales": "NET SALE VALUE",
        "total_mrp_sales": "MRP SALE VALUE",
        "brand": "BRAND"
    }
    return df.rename(columns=rename_map)


def load_zone_sales(brand: str) -> pd.DataFrame:
    df = _fetch_all_pages(
        "v_zone_sales", 
        brand, 
        "brand,f_year,zone,state,city,total_qty,total_net_sales,total_discount"
    )
    if df.empty:
        return df
        
    rename_map = {
        "f_year": "F_YEAR",
        "zone": "ZONE",
        "state": "STATE",
        "city": "CITY",
        "total_qty": "QTY SALE",
        "total_net_sales": "NET SALE VALUE",
        "total_discount": "DISCOUNT VALUE",
        "brand": "BRAND"
    }
    return df.rename(columns=rename_map)


def load_granular_data(brand: str, cols: list[str]) -> pd.DataFrame:
    # Map high-level pandas column names to db snake_case column names
    db_cols = []
    for col in cols:
        if col in COL_MAP:
            db_cols.append(COL_MAP[col])
        elif col.lower() in COL_MAP.values():
            db_cols.append(col.lower())
    
    # Always ensure brand is present
    if "brand" not in db_cols:
        db_cols.append("brand")
        
    select_query = ",".join(db_cols)
    df = _fetch_all_pages("sales_data", brand, select_query)
    if df.empty:
        return df
        
    # Rename back to original names expected by Python analytics
    df = df.rename(columns=REVERSE_COL_MAP)
    
    # Generate _MONTH helper if invoice_date is queried
    if "INVOICE DATE" in df.columns:
        df["INVOICE DATE"] = pd.to_datetime(df["INVOICE DATE"], errors="coerce")
        df["_MONTH"] = df["INVOICE DATE"].dt.to_period("M").astype(str)
        
    return df


def load_brand_data(
    brand: str
) -> pd.DataFrame:

    return load_granular_data(brand, COLS_TO_FETCH)


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

    # Keep only the first column if renaming created duplicate column names
    df = df.loc[:, ~df.columns.duplicated()]

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

    # Convert integer columns to Pandas nullable Int64 so they serialize to clean integers or null
    for col in ["qty_sale", "clsng_qty", "sr_no"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").round().astype("Int64")

    df = df.astype(object)

    df = df.replace(
        [np.nan, np.inf, -np.inf],
        None
    )

    rows = df.to_dict(
        orient="records"
    )

    CHUNK_SIZE = 1000

    inserted = 0

    progress_bar = st.progress(0)

    import time
    start_time = time.time()

    for i in range(
        0,
        len(rows),
        CHUNK_SIZE
    ):

        chunk = rows[
            i:i + CHUNK_SIZE
        ]

        chunk_start = time.time()
        try:

            result = (
                supabase
                .table("sales_data")
                .upsert(
                    chunk,
                    on_conflict="brand,bill_no,new_ean_code",
                    ignore_duplicates=True
                )
                .execute()
            )

            if result.data:
                inserted += len(
                    result.data
                )

            chunk_end = time.time()
            chunk_elapsed = chunk_end - chunk_start
            speed = len(chunk) / chunk_elapsed if chunk_elapsed > 0 else 0
            uploaded_so_far = min(i + CHUNK_SIZE, len(rows))
            
            progress_bar.progress(
                uploaded_so_far / len(rows),
                text=f"⚡ Uploading: {uploaded_so_far:,} / {len(rows):,} rows "
                     f"({uploaded_so_far / len(rows) * 100:.1f}%) | "
                     f"Speed: {speed:.0f} rows/sec"
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

    # Refresh materialized views database-side
    try:
        supabase.rpc("refresh_all_materialized_views").execute()
    except Exception as e:
        print(f"Warning: could not refresh materialized views: {e}")

    # Invalidate Streamlit cache to load new data immediately
    st.cache_data.clear()

    return {
        "inserted": inserted,
        "skipped": skipped
    }