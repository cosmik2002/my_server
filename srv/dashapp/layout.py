import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from datetime import timedelta, datetime


washes_layout = html.Div([
    html.Nav(html.A('Home', href='/')),
    html.H1('Выручка мойки'),
    dcc.Dropdown(
        id='wash-dropdown',
        options=[
            {'label': 'Beroun', 'value': 'Beroun'},
            {'label': 'Trutnov', 'value': 'Trutnov'},
            {'label': 'All', 'value': 'All'},
        ],
        value='Beroun'
    ),
    dcc.Dropdown(
        id='wash-time-dropdown',
        options=[
            {'label': 'По дням', 'value': 'days'},
            {'label': 'По часам', 'value': 'hours'},
        ],
        value='hours'
    ),
    dcc.Graph(
        id='wash-graph'
    )

])

layout = html.Div([
    html.Nav(html.A('Home', href='/')),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=datetime.now()-timedelta(5),
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
    dt.DataTable(id="data_table",
                 n_fixed_rows=1,
                 style_cell={
                     'whiteSpace': 'normal'
                 },
                 virtualization=True,pagination_mode=False),
    html.Div(id='content')
])#, style={'width': '500'})