from flask import render_template,current_app,request,Markup
import logging
from srv.main import bp
from srv import db, dash_app1
from flask_login import login_required,current_user
from datetime import datetime
import re

@bp.route('/dashtest')
def dash_test():
    cnt = dash_app1.index()
    #content = Markup(re.search(r'<body>(.+)</body>', cnt,re.DOTALL).group(1))
    content = re.search(r'<body>(.+)</body>', cnt,re.DOTALL).group(1)
    return render_template('dash.html',content=content)

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

@bp.route('/geo')
def geo():
    return render_template('geo.html')


@bp.before_app_request
def before_request():
  logging.getLogger('access_log').info('\t'.join([
            datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            request.headers.get('X-Forwarded-For',request.remote_addr),
            request.method,
            request.url,
            ', '.join(x+':'+request.values[x] for x in request.values),
            ', '.join([': '.join(x) for x in request.headers])]))
  if current_user.is_authenticated:
     current_user.last_seen = datetime.utcnow()
     db.session.commit()
