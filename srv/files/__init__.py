from flask import Blueprint

bp = Blueprint('files', __name__)

from srv.files import routes