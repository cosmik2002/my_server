import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
from srv.models import Operation, User
import plotly.graph_objs as go


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')



def generate_table(table):
    #d = []
    # for row in User.query.all():
    #     d.append({a: getattr(row, a) for a in User.__table__.columns.keys()})
    return dt.DataTable(
    id='my_table',
    columns=[{"name": i.key, "id": i.key} for i in table.__table__.columns if 'visible' not in i.info or i.info['visible'] is not False],
    data=[item.to_dict() for item in table.query.filter_by(wdate='25.02.2019',type_id=8)],
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
    )
], style={'width': '500'})

layout1 = html.Div([
    html.H1('Табличка'),
    generate_table(Operation)
], style={'width': '500'})