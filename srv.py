from srv import create_app, db
#from srv.models import User




app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)