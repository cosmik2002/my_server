from flask import render_template,current_app,request
from srv.fakturace import bp
from srv.models import knihafaktur
from flask_login import login_required,current_user
from flask_table import create_table, Table, Col
from sqlalchemy import desc


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    class ItemTable(Table):
        cislofa = Col('cislofa')
        numobjednavka = Col('numobjednavka')
    table_cls = create_table(options={'border': 'solid'})
    i = 0
    for col in knihafaktur.__table__.columns.keys():
        table_cls.add_column(col, Col(col))
        i = i+1
        # if i > 10:
        #     break
    # items = [dict(name='Name1', description='Description1'),
    #           dict(name='Name2', description='Description2'),
    #           dict(name='Name3', description='Description3')]
    items = knihafaktur.query.order_by(desc(knihafaktur.cislofa)).limit(50)
    table = table_cls(items)
    table1 = ItemTable(items)
    return render_template('table.html', table=table, table1=table1)
