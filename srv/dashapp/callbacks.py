from dash.dependencies import Input, Output, State
from srv.models import Climate, Operation
from sqlalchemy import or_, text
import dash_table as dtab

def register_callbacks(app):
   @app.callback(Output('my-graph','figure'),[Input('my-dropdown','value')])
   def upgrade_graph(value):
       figure = ''
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


def register_callbacks1(app):
    @app.callback(Output('table', 'children'),
                  [Input('button', 'n_clicks')],
                  [State('date-picker-range','start_date'),
                  State('date-picker-range','end_date')])
    def update_table(n_clicks,start_date,end_date):
        if n_clicks is None:
            return ''
        return dtab.DataTable(
            id='my_table',
            columns=[{"name": i.key, "id": i.key} for i in Operation.__table__.columns if
                     'visible' not in i.info or i.info['visible'] is not False],
            data=[item.to_dict() for item in Operation.query.filter(text("wdate between '"+start_date+"' and '"+end_date+"' and type_id=8"))],
            sorting=True,
            filtering=True
        )

