from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/hello")
# def hello():
#     return "Hello!"

@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name = None):
    return render_template("hello.html", name=name)

# Run Flask using python and the debug=True is when I make a change in the code, it will automatically refresh the info and reload to them for the website
# example of running with python ---> python3 main.py 
app.run(debug=True)