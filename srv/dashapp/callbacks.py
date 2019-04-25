from dash.dependencies import Input
from dash.dependencies import Output
from srv.models import Climate
from srv.models import Log
from sqlalchemy import or_, text,desc
from dateutil.tz import tzutc, tzlocal
import pandas as pd

def washes_register_callbacks(app,config):
    @app.callback(
         Output('wash-graph', 'figure'),
         [Input('wash-dropdown', 'value'),
          Input('wash-time-dropdown', 'value')]
    )
    def upgrade_graph(value,time):
        beroun_csv = config['BEROUN_CSV']
        trutnov_csv = config['TRUTNOV_CSV']
        if value != 'All':
            df = pd.read_csv(beroun_csv if value=='Beroun' else trutnov_csv, parse_dates=True, sep=';',index_col=0)
            df = df.ffill()
            if value == 'Beroun':
                df['val'] = (df['res'] - df['res'].shift(1))*10
            else:
                df['val'] = (df['res3'] - df['res3'].shift(1))
            if time == 'hours':
                data = df.resample('H')['val'].sum()
            if time == 'days':
                data = df.resample('D')['val'].sum()
            figure = {
                'data': [
                    {'x': [str(d.astimezone(tzlocal())) for d in data.keys()],
                     'y': [v for v in data],
                     'type': 'bar', 'name': 'Beroun'}
                ]
            }
        else:
            df1 = pd.read_csv(beroun_csv, parse_dates=True, sep=';', index_col=0)
            df2 = pd.read_csv(trutnov_csv, parse_dates=True, sep=';', index_col=0)
            df1 = df1.ffill()
            df2 = df2.ffill()
            df1['val'] = (df1['res'] - df1['res'].shift(1)) * 10
            df2['val'] = (df2['res3'] - df2['res3'].shift(1))
            if time == 'hours':
                data1 = df1.resample('H')['val'].sum()
                data2 = df2.resample('H')['val'].sum()
            if time == 'days':
                data1 = df1.resample('D')['val'].sum()
                data2 = df2.resample('D')['val'].sum()
            figure = {
                'data':[
                    {'x':[str(d.astimezone(tzlocal())) for d in data1.keys()],
                     'y':[v for v in data1],
                     'type': 'bar', 'name': 'Beroun'},
                    {'x': [str(d.astimezone(tzlocal())) for d in data2.keys()],
                     'y': [v for v in data2],
                     'type': 'bar', 'name': 'Trutnov'}

                ]
            }
        return figure



def register_callbacks(app):
   @app.callback(
       [Output('my-graph', 'figure'),
       Output('data_table', 'style_data_conditional'),
       Output('data_table', 'columns'),
       Output('data_table', 'data')],
       [Input('my-dropdown', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')])
   def upgrade_graph(value, start_date, end_date):
       figure = ''
       if value == 'temp':
         figure = {
          'data': [
             {'x': [str(i.date_time.replace(tzinfo=tzutc()).astimezone(tzlocal())) for i in Climate.query.filter(Climate.date_time >= start_date)],
              'y':[i.temp for i in Climate.query.filter(Climate.date_time >= start_date)], 'name':'Температура'}
          ]       
         } 
       if value == 'hum':
         figure = {
          'data': [
             {'x': [i.date_time.replace(tzinfo=tzutc()).astimezone(tzlocal()).strftime('%d.%m.%Y %H:%M') for i in Climate.query.filter(Climate.date_time >= start_date)],
              'y': [i.humidity for i in Climate.query.filter(Climate.date_time >= start_date)], 'name':'Влажность'}
          ]       
         } 
       if value == 'all':
         figure = {
          'data': [
             {'x': [i.date_time.replace(tzinfo=tzutc()) for i in Climate.query.filter(Climate.date_time >= start_date)],
              'y': [i.temp for i in Climate.query.filter(Climate.date_time >= start_date)], 'name':'Температура'},
             {'x': [i.date_time.replace(tzinfo=tzutc()) for i in Climate.query.filter(Climate.date_time >= start_date)],
              'y': [i.humidity for i in Climate.query.filter(Climate.date_time >= start_date)], 'name':'Влажность'}
          ]       
         }
       #columns = [{'id': 'Column 1', 'name': 'Column 1'}]
       #data = [{'Column 1': i} for i in range(3)]
       columns = [{"name": i.key, "id": i.key} for i in Log.__table__.columns if
                   'visible' not in i.info or i.info['visible'] is not False]
       data = [item.to_dict() for item in
                Log.query.order_by(desc(Log.date_time)).filter(Log.date_time >= start_date)]
       style_data_conditional = [
           {'if': {'column_id': 'date_time'},
            'width': '50px'},
           {'if': {'column_id': 'log_type'},
            'width': '50px'},
           {'if': {'column_id': 'message'},
            'width': '100px'}
       ]
       #filter(text("wdate between '" + start_date + "' and '" + end_date + "' and type_id=8"))],
       return figure,style_data_conditional,columns,data
