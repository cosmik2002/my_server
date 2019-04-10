from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/insCode.pl")
def insCode():
    return "Test World!"


if __name__ == "__main__":
    app.run()