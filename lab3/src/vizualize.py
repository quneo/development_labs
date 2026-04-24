import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

def get_income_sales_plots(df: pd.DataFrame):
    daily_by_category = df.groupby(['date', 'category']).agg({
        'income': 'sum',
        'sales': 'sum'
    }).reset_index()
    
    fig = make_subplots(rows=1, cols=2, 
                        subplot_titles=('Доход', 'Продажи'))

    for cat in daily_by_category['category'].unique():
        cat_data = daily_by_category[daily_by_category['category'] == cat]
        fig.add_scatter(x=cat_data['date'], y=cat_data['income'], 
                       name=cat, row=1, col=1, legendgroup=cat)
    
    for cat in daily_by_category['category'].unique():
        cat_data = daily_by_category[daily_by_category['category'] == cat]
        fig.add_scatter(x=cat_data['date'], y=cat_data['sales'], 
                       name=cat, row=1, col=2, legendgroup=cat, showlegend=False)
    
    fig.update_layout(height=800)
    return fig

def get_pie_charts(df: pd.DataFrame):
    region_stats = df[["region", "sales", "income"]].groupby("region").sum().reset_index()

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Продажи по регионам', 'Доход по регионам'),
        specs=[[{'type': 'pie'}, {'type': 'pie'}]]
    )

    fig.add_trace(
        go.Pie(
            labels=region_stats['region'],
            values=region_stats['sales'],
            name="Продажи"
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Pie(
            labels=region_stats['region'],
            values=region_stats['income'],
            name="Доход"
        ),
        row=1, col=2
    )

    return fig