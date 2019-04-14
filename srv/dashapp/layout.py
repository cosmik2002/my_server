import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from datetime import timedelta, datetime

layout = html.Div([
    html.Nav(html.A('Home', href='/')),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=datetime.now()-timedelta(30),
        end_date=datetime.now()
    ),
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
    ),
    dt.DataTable(id="data_table",virtualization=True,pagination_mode=False),
    html.Div(id='content')
])#, style={'width': '500'})