from flask import render_template,current_app,request
import logging
from re import match
from srv.dacha import bp
from srv import db
from srv.models import Climate,Log
from flask_login import login_required,current_user
from datetime import datetime

@bp.route('/')
@bp.route('/index')
def index():
    log_msg = request.args.get('log')
    if log_msg:
       if "temp" in log_msg:
          type = "climate"
          res = match(r'temp: (-*\d+) hum: (\d+)',log_msg)
          if res:
             db.session.add(Climate(type=1,temp=res.group(1),humidity=res.group(2)))          
       else:
          type = "log"
       db.session.add(Log(log_type = type,message = log_msg))
       db.session.commit()
       return request.args.get('log')
    return "dacha"

