from flask import Flask,render_template,request,jsonify,redirect,url_for
#import datafile
from database import load_members_from_db,load_member_from_db, commit_member_to_db

app = Flask(__name__)


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

@app.route("/viewmember/<id>")
def show_member(id):
  member = load_member_from_db(id)
  return render_template("viewmember.html", title="View Member",member=member)

@app.route("/editmember/<id>")
def edit_member(id):
  member = load_member_from_db(id)
  return render_template("editmember.html", title="Edit Member",member=member)

@app.route("/commitmember",methods =["POST"])
def commit_member():
  query = "update members set name ='" + request.form.get('nameInput') + "', company = '" + request.form.get('companyInput') + "', email ='" + request.form.get('emailInput') + "', phone = '" +  request.form.get('phoneInput') + "', nature = '" + request.form.get('natureInput') + "', address = '" + request.form.get('addressInput') + "' where ID= " + request.form.get('idInput')
  result = commit_member_to_db(query)
  return redirect(f"/viewmember/{request.form.get('idInput')}")
  
  
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
