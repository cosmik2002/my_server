from flask import render_template
from srv.files import bp
from flask_login import login_required


@bp.route('/')
@bp.route('/index')
@bp.route('/index/<string:file>')
@login_required
def index(file=''):
    files={"beroun.log": r"e:\Nicholas\python\tests\vnc\beroun.log","beroun.csv": r"e:\Nicholas\python\tests\vnc\beroun.csv","trutnov.csv": r"e:\Nicholas\python\tests\vnc\trutnov.csv"}
    text=''
    if file:
        f = open(files[file],'r')
        for line in f:
            text = text + line
        f.close()
    return render_template("file_show.html",files=("beroun.log","beroun.csv","trutnov.csv"),text=text)
