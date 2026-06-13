"""
analytics/product.py — Product / category analytics
"""

import pandas as pd
import numpy as np


def category_summary(df: pd.DataFrame, by: str = "MAIN CATEGORY") -> pd.DataFrame:
    return df.groupby(by, dropna=False).agg(
        revenue=("NET SALE VALUE", "sum"),
        units=("QTY SALE", "sum"),
        discount=("DISCOUNT VALUE", "sum"),
        mrp_value=("MRP SALE VALUE", "sum"),
        items=("ITEM NAME", "nunique"),
        clsng_qty=("CLSNG QTY", "sum"),
    ).reset_index().sort_values("revenue", ascending=False)


def brand_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("BRAND", dropna=False).agg(
        revenue=("NET SALE VALUE", "sum"),
        units=("QTY SALE", "sum"),
        discount=("DISCOUNT VALUE", "sum"),
        stores=("STORE CODE", "nunique"),
        items=("ITEM NAME", "nunique"),
    ).reset_index().sort_values("revenue", ascending=False)


def item_ranking(df: pd.DataFrame, top_n: int = 30) -> pd.DataFrame:
    return df.groupby(["ITEM NAME", "BRAND", "MAIN CATEGORY", "CATEGORY"], dropna=False).agg(
        revenue=("NET SALE VALUE", "sum"),
        units=("QTY SALE", "sum"),
        stores=("STORE CODE", "nunique"),
        avg_mrp=("MRP", "mean"),
    ).reset_index().sort_values("revenue", ascending=False).head(top_n)


def category_contribution(df: pd.DataFrame) -> pd.DataFrame:
    cat = category_summary(df)
    total_rev = cat["revenue"].sum()
    cat["contribution_pct"] = (cat["revenue"] / total_rev * 100).round(2)
    cat["cumulative_pct"]   = cat["contribution_pct"].cumsum().round(2)
    return cat


def monthly_category_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a pivot: index=_MONTH, columns=MAIN CATEGORY, values=revenue"""
    agg = df.groupby(["_MONTH", "MAIN CATEGORY"], dropna=False)["NET SALE VALUE"].sum().reset_index()
    pivot = agg.pivot(index="_MONTH", columns="MAIN CATEGORY", values="NET SALE VALUE").fillna(0)
    return pivot.sort_index()