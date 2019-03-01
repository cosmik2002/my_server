import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
from srv.models import Operation, User
import plotly.graph_objs as go


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')



def generate_table():
    #d = []
    # for row in User.query.all():
    #     d.append({a: getattr(row, a) for a in User.__table__.columns.keys()})
    return dt.DataTable(
    id='my_table',
    columns=[{"name": i.key, "id": i.key} for i in User.__table__.columns if 'visible' not in i.info],
    data=[item.to_dict() for item in User.query.all()],
    sorting=True,
    filtering=True
    )

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
    ),
    dt.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
    ), generate_table()], style={'width': '500'})