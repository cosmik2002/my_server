from file_read_backwards import FileReadBackwards
from flask import render_template, request, current_app
from srv.files import bp
from flask_login import login_required
import re

@bp.route('/')
@bp.route('/index')
@bp.route('/index/<string:file>')
@login_required
def index(file=''):
    files = current_app.config['FILES']
    text=''
    src = request.values.get("search_text") if request.values.get("search_text") else ''

    if file:
        # if 'log' in file:
        #     with FileReadBackwards(files[file], encoding="latin-1") as frb:
        #         c = 0
        #         for line in frb:
        #             src = request.values.get("search_text")
        #             if src:
        #                 if re.search(src, line):
        #                     text = text + line
        #             else:
        #                 text = text + line
        #             c = c + 1
        #             if c >= 500:
        #                 break
        # else:
            f = open(files[file], 'r')
            for line in f:
                if src:
                    if re.search(src, line):
                        text = text + line
                else:
                    text = text + line
            f.close()
    return render_template("file_show.html",files=files.keys(),text=text, src=src)
