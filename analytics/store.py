"""
analytics/store.py — Store-level aggregation helpers
"""

import pandas as pd
import numpy as np




def store_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return per-store KPI table."""
    agg = df.groupby(["STORE CODE", "NAME", "CITY", "STATE", "ZONE"], dropna=False).agg(
        revenue=("NET SALE VALUE", "sum"),
        units=("QTY SALE", "sum"),
        discount=("DISCOUNT VALUE", "sum"),
        mrp_value=("MRP SALE VALUE", "sum"),
        clsng_value=("CLSNG VALUE", "sum"),
        clsng_qty=("CLSNG QTY", "sum"),
        transactions=("BILL NO INVOICE NO", "nunique"),
    ).reset_index()

    agg["avg_ticket"]    = agg["revenue"] / agg["transactions"].replace(0, np.nan)
    agg["discount_pct"]  = agg["discount"] / agg["mrp_value"].replace(0, np.nan) * 100
    agg["sell_through"]  = agg["units"] / (agg["units"] + agg["clsng_qty"]).replace(0, np.nan) * 100

    # Performance score (0–100): weighted composite
    for col in ["revenue", "units", "sell_through"]:
        mn, mx = agg[col].min(), agg[col].max()
        rng = (mx - mn) if mx != mn else 1
        agg[f"_{col}_norm"] = (agg[col] - mn) / rng * 100

    agg["perf_score"] = (
        agg["_revenue_norm"]      * 0.50 +
        agg["_units_norm"]        * 0.30 +
        agg["_sell_through_norm"] * 0.20
    ).round(1)

    return agg.sort_values("revenue", ascending=False)


def store_monthly(df: pd.DataFrame, store_code: str) -> pd.DataFrame:
    sub = df[df["STORE CODE"] == store_code]
    return sub.groupby("_MONTH", dropna=False).agg(
        revenue=("NET SALE VALUE", "sum"),
        units=("QTY SALE", "sum"),
        discount=("DISCOUNT VALUE", "sum"),
    ).reset_index().sort_values("_MONTH")


def store_category_mix(df: pd.DataFrame, store_code: str) -> pd.DataFrame:
    sub = df[df["STORE CODE"] == store_code]
    return sub.groupby("MAIN CATEGORY", dropna=False).agg(
        revenue=("NET SALE VALUE", "sum"),
        units=("QTY SALE", "sum"),
    ).reset_index().sort_values("revenue", ascending=False)


def store_ranking(df: pd.DataFrame, metric: str = "revenue") -> pd.DataFrame:
    summary = store_summary(df)
    summary["rank"] = summary[metric].rank(ascending=False).astype(int)
    return summary.sort_values(metric, ascending=False)