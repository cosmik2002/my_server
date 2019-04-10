from srv import create_app, db
#from srv.models import User

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)