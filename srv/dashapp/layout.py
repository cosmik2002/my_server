import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime as dt


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')



def generate_table(table):
    #d = []
    # for row in User.query.all():
    #     d.append({a: getattr(row, a) for a in User.__table__.columns.keys()})
    return None

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

layout1 = html.Div([
    html.H1('Операции'),
    dcc.DatePickerRange(
    id='date-picker-range',
    start_date=dt.now(),
    end_date_placeholder_text='Select a date!'
    ),
    html.Button('Submit', id='button'),
    html.Div(id='table',style={'padding':'10px'})],style={'padding':'10px'})
    #generate_table(Operation)