from flask import render_template,current_app,request
import logging
from srv.fakturace import bp
from srv import db
from srv.models import knihafaktur
from flask_login import login_required,current_user
from datetime import datetime
from flask_table import create_table, Table, Col

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    class ItemTable(Table):
         cislofa = Col('cislofa')
         numobjednavka = Col('numobjednavka')
    tableCls = create_table(options={'border':'solid'})
    i=0
    for col in knihafaktur.__table__.columns.keys():
        tableCls.add_column(col,Col(col))
        i=i+1
        if i>10:
            break
    # items = [dict(name='Name1', description='Description1'),
    #           dict(name='Name2', description='Description2'),
    #           dict(name='Name3', description='Description3')]
    items = knihafaktur.query.limit(50)
    table = tableCls(items)
    table1 = ItemTable(items)
    return render_template('table.html', table=table, table1=table1)
