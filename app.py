from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/logincheck")
def check_login():
  return render_template("dashboard.html")

print(__name__)
if __name__ == "__main__" :
  app.run(host="0.0.0.0", debug=True)
