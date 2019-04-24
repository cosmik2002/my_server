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
@login_required
def index():
    return "washes"


