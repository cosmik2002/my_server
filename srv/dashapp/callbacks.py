from dash.dependencies import Input
from dash.dependencies import Output
from srv.models import Climate
from srv.models import Log
from sqlalchemy import or_, text,desc
from dateutil.tz import tzutc

def register_callbacks(app):
   @app.callback(
       [Output('my-graph','figure'),
       Output('data_table', 'columns'),
       Output('data_table', 'data')],
       [Input('my-dropdown','value')])
   # @app.callback(
   #       [Output('my-graph','figure'),
   #       Output('content', 'children')],
   #     [Input('my-dropdown','value')])
   def upgrade_graph(value):
       figure = '';
       if value =='temp':
         figure = {
          'data':[
             {'x':[i.date_time.replace(tzinfo=tzutc()) for i in Climate.query.all()],'y':[i.temp for i in Climate.query.all()],'name':'Температура'}
          ]       
         } 
       if value=='hum':
         figure = {
          'data':[
             {'x':[i.date_time.replace(tzinfo=tzutc()) for i in Climate.query.all()],'y':[i.humidity for i in Climate.query.all()],'name':'Влажность'}
          ]       
         } 
       if value=='all':
         figure = {
          'data':[
             {'x':[i.date_time.replace(tzinfo=tzutc()) for i in Climate.query.all()],'y':[i.temp for i in Climate.query.all()],'name':'Температура'},
             {'x':[i.date_time.replace(tzinfo=tzutc()) for i in Climate.query.all()],'y':[i.humidity for i in Climate.query.all()],'name':'Влажность'}
          ]       
         }
       #columns = [{'id': 'Column 1', 'name': 'Column 1'}]
       #data = [{'Column 1': i} for i in range(3)]
       columns = [{"name": i.key, "id": i.key} for i in Log.__table__.columns if
                   'visible' not in i.info or i.info['visible'] is not False]
       data = [item.to_dict() for item in
                Log.query.order_by(desc(Log.date_time)).all()]
       #filter(text("wdate between '" + start_date + "' and '" + end_date + "' and type_id=8"))],
       return figure,columns,data
