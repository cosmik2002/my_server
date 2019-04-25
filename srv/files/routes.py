from flask import render_template, request
from srv.files import bp
from flask_login import login_required
import re

@bp.route('/')
@bp.route('/index')
@bp.route('/index/<string:file>')
@login_required
def index(file=''):
    files={"beroun.log": r"e:\Nicholas\python\tests\vnc\beroun.log",
           "beroun.csv": r"e:\Nicholas\python\tests\vnc\beroun.csv",
           "trutnov.csv": r"e:\Nicholas\python\tests\vnc\trutnov.csv",
           "access.log": r"e:\Nicholas\python\my_server\logs\access.log"}
    text=''
    src = ''
    if file:
        f = open(files[file],'r')
        for line in f:
            src = request.values.get("search_text")
            if src:
                if re.search(src, line) :
                    text = text + line
            else:
                text = text + line
        f.close()
    return render_template("file_show.html",files=files.keys(),text=text, src=src)
