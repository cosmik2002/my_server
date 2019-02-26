from dash.dependencies import Input
from dash.dependencies import Output
from srv.models import Climate

def register_callbacks(app):
   @app.callback(Output('my-graph','figure'),[Input('my-dropdown','value')])
   def upgrade_graph(value):
       figure = '';
       if value =='temp':
         figure = {
          'data':[
             {'x':[i.date_time for i in Climate.query.all()],'y':[i.temp for i in Climate.query.all()],'name':'Температура'}
          ]       
         } 
       if value=='hum':
         figure = {
          'data':[
             {'x':[i.date_time for i in Climate.query.all()],'y':[i.humidity for i in Climate.query.all()],'name':'Влажность'}
          ]       
         } 
       if value=='all':
         figure = {
          'data':[
             {'x':[i.date_time for i in Climate.query.all()],'y':[i.temp for i in Climate.query.all()],'name':'Температура'},
             {'x':[i.date_time for i in Climate.query.all()],'y':[i.humidity for i in Climate.query.all()],'name':'Влажность'}
          ]       
         } 
       return figure
