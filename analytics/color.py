import pandas as pd


def color_performance(df):

    return (
        df.groupby("SHADE")
        .agg(
            revenue=("NET SALE VALUE", "sum"),
            units=("QTY SALE", "sum"),
            inventory=("CLSNG QTY", "sum")
        )
        .reset_index()
        .sort_values(
            "revenue",
            ascending=False
        )
    )


def top_colors(df):

    return color_performance(df).head(15)


def weak_colors(df):

    return color_performance(df).tail(15)


def color_by_state(df):

    return (
        df.groupby(
            ["STATE", "SHADE"]
        )["NET SALE VALUE"]
        .sum()
        .reset_index()
    )