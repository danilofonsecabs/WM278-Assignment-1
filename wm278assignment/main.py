from flask import Flask
from markupsafe import escape

app = Flask(__name__)

if __name__ == "__main__":
    app.run()

@app.route("/")
def home():
    return "Hello! this is the main page <h1>HELLO</h1>"