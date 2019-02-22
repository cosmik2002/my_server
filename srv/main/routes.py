from flask import render_template,current_app,request
import logging
from srv.main import bp
from srv import db
from flask_login import login_required,current_user
from datetime import datetime

@bp.route('/')
@bp.route('/index')
@login_required	
def index():
    user = {'username': 'Nicholas'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }, 
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@bp.before_app_request
def before_request():
  logging.getLogger('access_log').info('\t'.join([
            datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            request.remote_addr,
            request.method,
            request.url,
            ', '.join(x+':'+request.values[x] for x in request.values),
            ', '.join([': '.join(x) for x in request.headers])]))
  if current_user.is_authenticated:
     current_user.last_seen = datetime.utcnow()
     db.session.commit()
