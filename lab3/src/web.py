from dash import Dash, Input, Output, html, dcc, dash_table, callback
import pandas as pd
from plotly.subplots import make_subplots
from queries import filterQuerySet
from vizualize import get_income_sales_plots, get_pie_charts
from data_generate import CategoryName, Region

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Анализ продаж', style={'text-align': 'center'}),
    
    html.Div([
        html.Div([
            html.Label('Период:'),
            dcc.DatePickerRange(
                id='date-range',
                start_date='2025-01-01',
                end_date='2025-12-31',
                display_format='YYYY-MM-DD'
            )
        ], style={'margin': '10px'}),
        
        html.Div([
            html.Label('Категории:'),
            dcc.Dropdown(
                id='category-dropdown',
                options=[{'label': cat.value, 'value': cat.value} 
                        for cat in CategoryName],
                value=[cat.value for cat in CategoryName],
                multi=True,
                style={'width': '300px'}
            )
        ], style={'margin': '10px'}),
        
        html.Div([
            html.Label('Регионы:'),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': reg.value, 'value': reg.value} 
                        for reg in Region],
                value=[reg.value for reg in Region],
                multi=True,
                style={'width': '300px'}
            )
        ], style={'margin': '10px'}),
        
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '20px', 'padding': '20px'}),
    
    html.H3('Линейные графики (доход/продажи по категориям)', style={'text-align': 'center'}),
    dcc.Graph(id='line-plot'),
    
    html.H3('Круговые диаграммы (по регионам)', style={'text-align': 'center', 'margin-top': '40px'}),
    dcc.Graph(id='pie-plot'),

    html.H3('Таблица с детализацией данных', style={'text-align': 'center', 'margin-top': '40px'}),

    dash_table.DataTable(
        id='detail-table',
        page_size=15,
        sort_action='native',
        filter_action='native',
        style_table={'overflowX': 'auto', 'padding': '0 20px'},
        style_cell={
            'textAlign': 'left',
            'padding': '8px',
            'minWidth': '120px',
            'width': '120px',
            'maxWidth': '250px',
            'whiteSpace': 'normal'
        },
        style_header={
            'fontWeight': 'bold',
            'backgroundColor': '#f2f2f2'
        }
    )
])

@callback(
    [Output('line-plot', 'figure'),
     Output('pie-plot', 'figure'),
     Output('detail-table', 'data'),
     Output('detail-table', 'columns')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('category-dropdown', 'value'),
     Input('region-dropdown', 'value')]
)
def update_dashboard(start_date, end_date, categories, regions):
    start = pd.to_datetime(start_date) if start_date else None
    end = pd.to_datetime(end_date) if end_date else None

    cat_enums = [CategoryName(cat) for cat in categories] if categories else None
    reg_enums = [Region(reg) for reg in regions] if regions else None

    filtered_df = filterQuerySet(
        start_date=start,
        end_date=end,
        categories=cat_enums,
        regions=reg_enums
    )

    if filtered_df.empty:
        empty_fig = make_subplots(rows=1, cols=2)
        empty_fig.add_annotation(
            text="Нет данных",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False
        )
        return empty_fig, empty_fig, [], []

    line_fig = get_income_sales_plots(filtered_df)
    pie_fig = get_pie_charts(filtered_df)

    table_df = filtered_df.copy()

    if 'date' in table_df.columns:
        table_df['date'] = pd.to_datetime(table_df['date']).dt.strftime('%Y-%m-%d')

    data = table_df.to_dict('records')
    columns = [{'name': col, 'id': col} for col in table_df.columns]

    return line_fig, pie_fig, data, columns
