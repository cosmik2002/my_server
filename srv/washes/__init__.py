from flask import Blueprint

bp = Blueprint('washes', __name__)

from srv.washes import routes