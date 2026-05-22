from pathlib import Path
from io import StringIO
import base64

from dash import Dash, Input, Output, State, html, dcc, dash_table, callback
import pandas as pd
import plotly.graph_objects as go

from data_generate import StationName, generate_passenger_flow, save_csv
from queries import filter_dataframe, get_all_data
from vizualize import get_time_series_plot, get_heatmap, get_scatter_plot


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "passenger_flow.csv"
AUTHOR_PHOTO_PATH = BASE_DIR / "data" / "ava.jpg"
DEFAULT_STATIONS = [
    StationName.central.value,
    StationName.east.value,
    StationName.west.value,
]
DEFAULT_HOUR = 8


def prepare_data() -> None:
    if not DATA_PATH.exists():
        data = generate_passenger_flow()
        save_csv(data, str(DATA_PATH))


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


def dataframe_to_store(data: pd.DataFrame) -> str:
    return data.to_json(date_format="iso", orient="split")


def dataframe_from_store(data_json: str) -> pd.DataFrame:
    data = pd.read_json(StringIO(data_json), orient="split")
    data["date"] = pd.to_datetime(data["date"])
    return data


def nav_link(text: str, href: str):
    return dcc.Link(
        text,
        href=href,
        style={
            "padding": "10px 16px",
            "textDecoration": "none",
            "color": "white",
            "backgroundColor": "#3164a8",
            "borderRadius": "6px",
            "display": "inline-block"
        }
    )


def get_author_photo_src():
    if not AUTHOR_PHOTO_PATH.exists():
        return None

    encoded_photo = base64.b64encode(AUTHOR_PHOTO_PATH.read_bytes()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded_photo}"


def get_filters(stations=None, hour=None):
    return html.Div([
        html.Div([
            html.Label("Станции:"),
            dcc.Dropdown(
                id="station-dropdown",
                options=[{"label": station.value, "value": station.value} for station in StationName],
                value=stations or DEFAULT_STATIONS,
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
                value=hour if hour is not None else DEFAULT_HOUR,
                marks={hour_value: str(hour_value) for hour_value in range(0, 24, 2)},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={"margin": "10px", "width": "500px"}),
    ], style={"display": "flex", "flexWrap": "wrap", "gap": "20px", "padding": "20px"})


def get_first_page(filters):
    stations = filters.get("stations", DEFAULT_STATIONS) if filters else DEFAULT_STATIONS
    hour = filters.get("hour", DEFAULT_HOUR) if filters else DEFAULT_HOUR

    return html.Div([
        get_filters(stations, hour),

        html.H3(
            "Временной ряд по выбранным станциям и часу",
            style={"textAlign": "center"}
        ),
        dcc.Graph(id="time-series-plot"),

        html.H3(
            "Таблица с данными",
            style={"textAlign": "center", "marginTop": "40px"}
        ),
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


def get_second_page():
    return html.Div([
        html.H3(
            "Тепловая карта пассажиропотока",
            style={"textAlign": "center"}
        ),
        dcc.Graph(id="heatmap-plot"),

        html.H3(
            "Диаграмма рассеяния",
            style={"textAlign": "center", "marginTop": "40px"}
        ),
        dcc.Graph(id="scatter-plot")
    ])


def get_author_page():
    photo_src = get_author_photo_src()

    return html.Div([
        html.H2("Информация об авторе", style={"textAlign": "center"}),
        html.Div([
            html.Img(
                src=photo_src,
                style={
                    "width": "180px",
                    "height": "180px",
                    "objectFit": "cover",
                    "borderRadius": "8px",
                    "display": "block",
                    "margin": "0 auto 20px auto"
                }
            ) if photo_src else html.Div(),
            html.H3("Никитин Вадим", style={"textAlign": "center"}),
            html.P("Лабораторная работа №5"),
            html.P("Тема: многостраничное приложение Dash для анализа пассажиропотока."),
            html.P("Данные генерируются автоматически и сохраняются в CSV."),
        ], style={
            "maxWidth": "700px",
            "margin": "20px auto",
            "fontSize": "18px",
            "lineHeight": "1.6"
        })
    ])


prepare_data()
app = Dash(__name__, suppress_callback_exceptions=True)


app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id="data-store"),
    dcc.Store(id="filter-store", data={"stations": DEFAULT_STATIONS, "hour": DEFAULT_HOUR}),

    html.H1("Анализ пассажиропотока", style={"textAlign": "center"}),

    html.Div([
        nav_link("Временной ряд", "/"),
        nav_link("Графики", "/charts"),
        nav_link("Автор", "/author"),
    ], style={
        "display": "flex",
        "justifyContent": "center",
        "gap": "12px",
        "padding": "12px",
        "flexWrap": "wrap"
    }),

    html.Div(id="page-content")
])


@callback(
    Output("data-store", "data"),
    Input("url", "pathname")
)
def load_data(pathname):
    data = get_all_data(str(DATA_PATH))
    return dataframe_to_store(data)


@callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    State("filter-store", "data")
)
def display_page(pathname, filters):
    if pathname == "/charts":
        return get_second_page()

    if pathname == "/author":
        return get_author_page()

    return get_first_page(filters)


@callback(
    Output("filter-store", "data"),
    [Input("station-dropdown", "value"),
     Input("hour-slider", "value")],
    prevent_initial_call=True
)
def update_filters(stations, hour):
    return {
        "stations": stations or [],
        "hour": hour
    }


@callback(
    [Output("time-series-plot", "figure"),
     Output("detail-table", "data"),
     Output("detail-table", "columns")],
    [Input("data-store", "data"),
     Input("filter-store", "data")]
)
def update_first_page(data_json, filters):
    if not data_json:
        return get_empty_figure(), [], []

    data = dataframe_from_store(data_json)
    stations = filters.get("stations") if filters else DEFAULT_STATIONS
    hour = filters.get("hour") if filters else DEFAULT_HOUR

    filtered_df = filter_dataframe(data, stations=stations, hour=hour)

    if filtered_df.empty:
        return get_empty_figure(), [], []

    time_series_fig = get_time_series_plot(filtered_df)

    table_df = filtered_df.copy()
    table_df["date"] = pd.to_datetime(table_df["date"]).dt.strftime("%Y-%m-%d")

    table_data = table_df.to_dict("records")
    columns = [{"name": col, "id": col} for col in table_df.columns]

    return time_series_fig, table_data, columns


@callback(
    [Output("heatmap-plot", "figure"),
     Output("scatter-plot", "figure")],
    [Input("data-store", "data"),
     Input("filter-store", "data")]
)
def update_second_page(data_json, filters):
    if not data_json:
        empty_fig = get_empty_figure()
        return empty_fig, empty_fig

    data = dataframe_from_store(data_json)
    stations = filters.get("stations") if filters else DEFAULT_STATIONS
    filtered_df = filter_dataframe(data, stations=stations)

    if filtered_df.empty:
        empty_fig = get_empty_figure()
        return empty_fig, empty_fig

    heatmap_fig = get_heatmap(filtered_df)
    scatter_fig = get_scatter_plot(filtered_df)

    return heatmap_fig, scatter_fig
