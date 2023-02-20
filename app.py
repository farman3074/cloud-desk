from flask import Flask,render_template,request
from sqlalchemy import text
#import datafile
from database import engine

app = Flask(__name__)

def load_members_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from members"))
    mem_list = result.all()
    members = []
    for row in mem_list:
      members.append(row._mapping)
    return members

@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/logincheck",methods =["POST"])
def check_login():
  user = request.form.get("username") 
  if  user == "farman":
      return render_template("dashboard.html", title="Dash Board")
  else:
    return render_template("home.html")

@app.route("/dashboard")
def show_dashbaord():
  return render_template("dashboard.html", title="Dash Board")


@app.route("/members")
def show_members():
  members = load_members_from_db()
  return render_template("members.html", title="Members", members=members)

@app.route("/spaces")
def show_spaces():
  return render_template("spaces.html", title="Spaces")

@app.route("/invoicing")
def show_invoices():
  return render_template("invoicing.html", title="Invoicing")

@app.route("/reporting")
def show_reporting():
  return render_template("reporting.html", title="Reporting")


print(__name__)
if __name__ == "__main__" :
  app.run(host="0.0.0.0", debug=True)
