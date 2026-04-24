import pandas as pd
import plotly.express as px


def get_time_series_plot(df: pd.DataFrame):
    daily_data = df.groupby(["date", "station"]).agg({
        "passengers": "sum"
    }).reset_index()

    fig = px.line(
        daily_data,
        x="date",
        y="passengers",
        color="station",
        markers=True,
        title="Динамика пассажиропотока"
    )

    fig.update_layout(height=500)
    return fig


def get_heatmap(df: pd.DataFrame):
    heatmap_data = df.groupby(["station", "hour"]).agg({
        "passengers": "mean"
    }).reset_index()

    table = heatmap_data.pivot(
        index="station",
        columns="hour",
        values="passengers"
    )

    fig = px.imshow(
        table,
        labels=dict(x="Час", y="Станция", color="Пассажиры"),
        title="Средний пассажиропоток по станциям и часам",
        aspect="auto"
    )

    fig.update_layout(height=500)
    return fig


def get_scatter_plot(df: pd.DataFrame):
    scatter_data = df.groupby(["station", "hour"]).agg({
        "passengers": "mean"
    }).reset_index()

    fig = px.scatter(
        scatter_data,
        x="hour",
        y="passengers",
        color="station",
        size="passengers",
        title="Зависимость пассажиропотока от времени суток"
    )

    fig.update_layout(height=500)
    return fig
