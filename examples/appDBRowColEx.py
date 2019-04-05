import sys
sys.path.insert(0, r'E:\Nicholas\python\my_server')
#sys.path.insert(0, r'C:\server\my_server')
from srv import create_app, db
from srv.models import User

app = create_app()

with app.app_context():
 d={a:[] for a in User.__table__.columns.keys()}
 for row in User.query.all():
    for key in User.__table__.columns.keys():
      d[key].append(getattr(row,key))
print('%s',d)