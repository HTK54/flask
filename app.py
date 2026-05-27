from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    print("홈")
    return render_template("index.html")

@app.route("/aa")
def aa():
    print("aa")
    return "aa"

@app.route("/bb")
def bb():
    print("bb")
    return "bb"


app.run(debug=True)
