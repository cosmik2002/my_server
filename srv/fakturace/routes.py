from flask import render_template,current_app,request
import logging
from srv.fakturace import bp
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
