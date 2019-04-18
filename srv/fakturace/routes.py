from flask import render_template, current_app, request
from srv.fakturace import bp
from srv.models import knihafaktur, adresy, odberatele_311, knihafakturpolozky
from srv import db
from flask_login import login_required, current_user
from flask_table import create_table, Table, Col, LinkCol
from sqlalchemy import desc, literal
from sqlalchemy.orm import load_only
from sqlalchemy.sql.expression import  label
from flask import Markup
import pandas


@bp.route('/')
@bp.route('/index')
@bp.route('/index/<int:page>')
@login_required
def index(page=1):
    per_page = 15
    q = knihafaktur.query.order_by(desc(knihafaktur.cislofa)).join("adresy"). \
        join(odberatele_311, knihafaktur.indexzaznamu == odberatele_311.indexzaznamu). \
        with_entities(knihafaktur.cislofa, knihafaktur.datumspla.label("Splatnost"),
                      knihafaktur.sumcelkemkuhrade.label("Castka"), odberatele_311.celkemdal.label("Zaplaceno"), odberatele_311.mena.label("Mena"),
                      adresy.nazevfirmy.label("Firma"))
    paginate = q.paginate(page, per_page, False)
    table_cls = create_table(options={'classes': ['table','table-hover']})
    table_cls.add_column("link", LinkCol("Faktura", "fakturace.spec", attr="cislofa", url_kwargs=dict(cislofa='cislofa')))
    for col in q.column_descriptions:
        table_cls.add_column(col["name"], Col(col["name"]))
    table_cls._cols['cislofa'].show=False
    table = table_cls(paginate.items)
    return render_template('fakturace.html', table=table, kniha=paginate)


@bp.route('/spec/<int:cislofa>')
@login_required
def spec(cislofa=1):
    q = knihafakturpolozky.query.filter(knihafakturpolozky.cislofaktury == cislofa).\
        with_entities(knihafakturpolozky.cisloradku.label("N"),knihafakturpolozky.textpolozky.label("Polozka"),
                      knihafakturpolozky.jednotkovacena.label("JednCena"),knihafakturpolozky.mnozstvi.label("Mnozstvi"),
                      knihafakturpolozky.mernajednotka.label("Mj"),
                      label('CelkCena', knihafakturpolozky.jednotkovacena * knihafakturpolozky.mnozstvi))
    table_cls = create_table(options={'classes': ['table','table-hover']})
    for col in q.column_descriptions:
        table_cls.add_column(col["name"], Col(col["name"]))
    table = table_cls(q.all())
    return render_template('fakturace_spec.html', table=table)
