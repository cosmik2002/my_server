from waitress import serve
from srv import create_app
import logging
app = create_app()
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)
serve(app)