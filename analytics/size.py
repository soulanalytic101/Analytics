import pandas as pd


def size_performance(df):

    return (
        df.groupby("SIZE")
        .agg(
            revenue=("NET SALE VALUE", "sum"),
            units=("QTY SALE", "sum"),
            inventory=("CLSNG QTY", "sum")
        )
        .reset_index()
        .sort_values(
            "units",
            ascending=False
        )
    )


def best_sizes(df):

    return (
        size_performance(df)
        .head(10)
    )


def dead_sizes(df):

    sizes = size_performance(df)

    sizes["dead_ratio"] = (
        sizes["inventory"] /
        (sizes["units"] + 1)
    )

    return sizes.sort_values(
        "dead_ratio",
        ascending=False
    ).head(10)
    

def size_heatmap(df):

    return pd.pivot_table(
        df,
        index="CATEGORY",
        columns="SIZE",
        values="QTY SALE",
        aggfunc="sum",
        fill_value=0
    )