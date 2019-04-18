from dash.dependencies import Input
from dash.dependencies import Output
from srv.models import Climate
from srv.models import Log
from sqlalchemy import or_, text,desc
from dateutil.tz import tzutc, tzlocal

def register_callbacks(app):
   @app.callback(
       [Output('my-graph', 'figure'),
       Output('data_table', 'columns'),
       Output('data_table', 'data')],
       [Input('my-dropdown', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')])
   # @app.callback(
   #       [Output('my-graph','figure'),
   #       Output('content', 'children')],
   #     [Input('my-dropdown','value')])
   def upgrade_graph(value, start_date, end_date):
       figure = ''
       if value == 'temp':
         figure = {
          'data': [
             {'x': [i.date_time.replace(tzinfo=tzutc()).astimezone(tzlocal()) for i in Climate.query.filter(Climate.date_time >= start_date)],
              'y':[i.temp for i in Climate.query.filter(Climate.date_time >= start_date)], 'name':'Температура'}
          ]       
         } 
       if value == 'hum':
         figure = {
          'data': [
             {'x': [i.date_time.replace(tzinfo=tzutc()) for i in Climate.query.filter(Climate.date_time >= start_date)],
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
       #filter(text("wdate between '" + start_date + "' and '" + end_date + "' and type_id=8"))],
       return figure,columns,data
