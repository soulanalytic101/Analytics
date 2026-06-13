import pandas as pd


def generate_recommendations(df):

    recommendations = []

    # Best Size

    size_sales = (
        df.groupby("SIZE")["QTY SALE"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    if len(size_sales):

        best_size = size_sales.index[0]

        recommendations.append(
            f"Increase inventory for Size {best_size}"
        )

    # Best Color

    color_sales = (
        df.groupby("SHADE")["NET SALE VALUE"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    if len(color_sales):

        best_color = color_sales.index[0]

        recommendations.append(
            f"{best_color} is the highest revenue generating color"
        )

    # Dead Stock

    dead = df[
        (df["CLSNG QTY"] > 20)
        &
        (df["QTY SALE"] == 0)
    ]

    if len(dead):

        recommendations.append(
            f"{len(dead)} SKUs identified as dead stock"
        )

    # Best Store

    stores = (
        df.groupby("NAME")
        ["NET SALE VALUE"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    if len(stores):

        best_store = stores.index[0]

        recommendations.append(
            f"{best_store} is the highest performing store"
        )

    return recommendations