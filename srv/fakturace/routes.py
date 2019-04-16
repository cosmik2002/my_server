from flask import render_template,current_app,request
from srv.fakturace import bp
from srv.models import knihafaktur, adresy
from srv import db
from flask_login import login_required,current_user
from flask_table import create_table, Table, Col
from sqlalchemy import desc
from sqlalchemy.orm import load_only
import pandas



@bp.route('/')
@bp.route('/index')
@bp.route('/index/<int:page>')
@login_required
def index(page=1):
    per_page = 10
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
    # df = pandas.read_sql(knihafaktur.query.join(adresy).order_by(desc(knihafaktur.cislofa))
    #                      .add_columns(adresy.nazevfirmy).limit(50).statement,db.get_engine(bind='fakturace'))
    stmt = knihafaktur.query.order_by(desc(knihafaktur.cislofa)).from_self(knihafaktur.cislofa,adresy.nazevfirmy).\
        join(adresy).statement
    stmt = knihafaktur.query.order_by(desc(knihafaktur.cislofa)).options(load_only("cislofa")).join("adresy").statement
    stmt = knihafaktur.query.order_by(desc(knihafaktur.cislofa)).join("adresy").with_entities(knihafaktur.cislofa,adresy.nazevfirmy).statement
    df = pandas.read_sql(knihafaktur.query.order_by(desc(knihafaktur.cislofa)).from_self(knihafaktur.cislofa,adresy.nazevfirmy).
                         join(adresy).limit(per_page).offset(page*per_page).statement,db.get_engine(bind='fakturace'))
    df = pandas.read_sql(stmt, db.get_engine(bind='fakturace'))
    table_cls_pd = create_table(options={'border': 'solid'})
    for col in df.columns:
        table_cls_pd.add_column(col, Col(col))

    items = knihafaktur.query.order_by(desc(knihafaktur.cislofa)).limit(50)
    table = table_cls(items)
    table1 = ItemTable(items)
    table2 = table_cls_pd(df.to_dict('rows'))
    return render_template('fakturace.html', table=table2)
