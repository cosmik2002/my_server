from flask import Blueprint

bp = Blueprint('fakturace', __name__)

from srv.fakturace import routes