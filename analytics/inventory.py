import pandas as pd
import numpy as np


def inventory_summary(df):

    return df.groupby(
        ["MAIN CATEGORY"],
        dropna=False
    ).agg(
        inventory_qty=("CLSNG QTY", "sum"),
        inventory_value=("CLSNG VALUE", "sum"),
        sales_qty=("QTY SALE", "sum"),
        revenue=("NET SALE VALUE", "sum")
    ).reset_index()


def dead_stock(df, min_inventory=10):

    dead = df[
        (df["CLSNG QTY"] > min_inventory)
        & (df["QTY SALE"] <= 0)
    ]

    return dead.sort_values(
        "CLSNG VALUE",
        ascending=False
    )


def fast_movers(df):

    fast = df.copy()

    fast["velocity"] = (
        fast["QTY SALE"] /
        (fast["CLSNG QTY"] + 1)
    )

    return fast.sort_values(
        "velocity",
        ascending=False
    ).head(50)


def slow_movers(df):

    slow = df.copy()

    slow["velocity"] = (
        slow["QTY SALE"] /
        (slow["CLSNG QTY"] + 1)
    )

    return slow.sort_values(
        "velocity",
        ascending=True
    ).head(50)


def inventory_health_score(df):

    sold = df["QTY SALE"].sum()
    stock = df["CLSNG QTY"].sum()

    if sold + stock == 0:
        return 0

    return round(
        sold / (sold + stock) * 100,
        2
    )