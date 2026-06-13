import pandas as pd


def state_performance(df):

    return (
        df.groupby("STATE")
        .agg(
            revenue=("NET SALE VALUE", "sum"),
            units=("QTY SALE", "sum"),
            stores=("STORE CODE", "nunique")
        )
        .reset_index()
        .sort_values(
            "revenue",
            ascending=False
        )
    )


def zone_performance(df):

    return (
        df.groupby("ZONE")
        .agg(
            revenue=("NET SALE VALUE", "sum"),
            units=("QTY SALE", "sum"),
            stores=("STORE CODE", "nunique")
        )
        .reset_index()
        .sort_values(
            "revenue",
            ascending=False
        )
    )


def city_performance(df):

    return (
        df.groupby("CITY")
        .agg(
            revenue=("NET SALE VALUE", "sum"),
            units=("QTY SALE", "sum")
        )
        .reset_index()
        .sort_values(
            "revenue",
            ascending=False
        )
    )