from pathlib import Path

from dash import Dash, Input, Output, html, dcc, dash_table, callback
import pandas as pd
import plotly.graph_objects as go

from data_generate import StationName, generate_passenger_flow, save_csv
from queries import filterQuerySet, get_all_data
from vizualize import get_time_series_plot, get_heatmap, get_scatter_plot


DATA_PATH = Path("data/passenger_flow.csv")


def prepare_data() -> None:
    if not DATA_PATH.exists():
        data = generate_passenger_flow()
        save_csv(data)


prepare_data()
app = Dash(__name__)


app.layout = html.Div([
    html.H1("Анализ пассажиропотока", style={"text-align": "center"}),

    html.Div([
        html.Div([
            html.Label("Станции:"),
            dcc.Dropdown(
                id="station-dropdown",
                options=[{"label": station.value, "value": station.value} for station in StationName],
                value=[StationName.central.value, StationName.east.value, StationName.west.value],
                multi=True,
                style={"width": "400px"}
            )
        ], style={"margin": "10px"}),

        html.Div([
            html.Label("Время суток:"),
            dcc.Slider(
                id="hour-slider",
                min=0,
                max=23,
                step=1,
                value=8,
                marks={hour: str(hour) for hour in range(0, 24, 2)},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={"margin": "10px", "width": "500px"}),
    ], style={"display": "flex", "flex-wrap": "wrap", "gap": "20px", "padding": "20px"}),

    html.H3("Временной ряд по выбранным станциям и часу", style={"text-align": "center"}),
    dcc.Graph(id="time-series-plot"),

    html.H3("Тепловая карта пассажиропотока", style={"text-align": "center", "margin-top": "40px"}),
    dcc.Graph(id="heatmap-plot"),

    html.H3("Диаграмма рассеяния", style={"text-align": "center", "margin-top": "40px"}),
    dcc.Graph(id="scatter-plot"),

    html.H3("Таблица с данными", style={"text-align": "center", "margin-top": "40px"}),
    dash_table.DataTable(
        id="detail-table",
        page_size=15,
        sort_action="native",
        filter_action="native",
        style_table={"overflowX": "auto", "padding": "0 20px 20px 20px"},
        style_cell={
            "textAlign": "left",
            "padding": "8px",
            "minWidth": "120px",
            "width": "120px",
            "maxWidth": "250px",
            "whiteSpace": "normal"
        },
        style_header={
            "fontWeight": "bold",
            "backgroundColor": "#f2f2f2"
        }
    )
])


def get_empty_figure():
    fig = go.Figure()
    fig.add_annotation(
        text="Нет данных",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False
    )
    return fig


@callback(
    [Output("time-series-plot", "figure"),
     Output("heatmap-plot", "figure"),
     Output("scatter-plot", "figure"),
     Output("detail-table", "data"),
     Output("detail-table", "columns")],
    [Input("station-dropdown", "value"),
     Input("hour-slider", "value")]
)
def update_dashboard(stations, hour):
    filtered_df = filterQuerySet(stations=stations, hour=hour)

    if filtered_df.empty:
        empty_fig = get_empty_figure()
        return empty_fig, empty_fig, empty_fig, [], []

    all_data = get_all_data()

    heatmap_df = all_data[all_data["station"].isin(stations)] if stations else all_data
    scatter_df = heatmap_df.copy()

    time_series_fig = get_time_series_plot(filtered_df)
    heatmap_fig = get_heatmap(heatmap_df)
    scatter_fig = get_scatter_plot(scatter_df)

    table_df = filtered_df.copy()
    table_df["date"] = pd.to_datetime(table_df["date"]).dt.strftime("%Y-%m-%d")

    data = table_df.to_dict("records")
    columns = [{"name": col, "id": col} for col in table_df.columns]

    return time_series_fig, heatmap_fig, scatter_fig, data, columns
