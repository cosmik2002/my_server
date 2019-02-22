from flask import Blueprint

bp = Blueprint('dacha', __name__,template_folder='templates')

from srv.dacha import routes