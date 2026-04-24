from dash import Dash, Input, Output, html, dcc
from plot import get_plot


app = Dash()

app.layout = [
    html.Div(
        children=[
            html.Div('Plotly Dash', className="app-header--title")
        ]
    ),
    dcc.Graph(id="plot", figure={}),
    dcc.Checklist(id="show_plots", options=["show_first", "show_second"])
]


@app.callback(
    Output(component_id='plot', component_property='figure'),
    Input(component_id='show_plots', component_property='value')
)
def update_graph(options):
    print(options)
    opt1 = 'show_first' in options if options else False
    opt2 = 'show_second' in options if options else False
    print([opt1, opt2])
    fig = get_plot(show_first=opt1, show_second=opt2)
    return fig