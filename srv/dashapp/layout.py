import dash_core_components as dcc
import dash_html_components as html
from srv.models import Climate
import plotly.graph_objs as go

layout = html.Div([
    html.H1('Температура на дачке'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Температура', 'value': 'temp'},
            {'label': 'Влажность', 'value': 'hum'},
            {'label': 'Все вместе', 'value': 'all'},
        ],
        value='temp'
    ),
    dcc.Graph(
       id='my-graph'
    )
], style={'width': '500'})