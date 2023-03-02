from flask import Flask,render_template,request,jsonify,redirect,url_for
#import datafile
from datetime import datetime
from database import load_members_from_db,load_member_from_db, commit_member_to_db, load_spaces_from_db, load_space_from_db, commit_space_to_db, commit_booking_to_db,commit_ledger_to_db

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
  spaces = load_spaces_from_db()
  return render_template("spaces.html", title="Spaces", spaces=spaces)

@app.route("/viewspace/<id>")
def show_space(id):
  space = load_space_from_db(id)
  return render_template("viewspace.html", title="View Space",space=space)

@app.route("/editspace/<id>")
def edit_space(id):
  space = load_space_from_db(id)
  return render_template("editspace.html", title="Edit space",space=space)

@app.route("/commitspace",methods =["POST"])
def commit_space():
  query = "update spaces set name ='" + request.form.get('nameInput') + "', type = '" + request.form.get('typeInput') + "', floor ='" + request.form.get('floorInput') + "', seats = " +  request.form.get('seatsInput') + ", area = " + request.form.get('areaInput') + ", isempty = '" + request.form.get('emptyInput') + "' where ID= " + request.form.get('idInput')
  result = commit_space_to_db(query)
  return redirect(f"/viewspace/{request.form.get('idInput')}")

@app.route("/bookspace/<id>")
def book_space(id):
  space = load_space_from_db(id)
  members = load_members_from_db()
  currentdate = datetime.now().date()
  return render_template("bookspace.html", title = "Book " + space['name'], space=space, members=members, currentdate = currentdate)

@app.route("/commitbooking",methods =["POST"])
def commit_booking():
  query = "insert into bookings (memberID, spaceID, bookFrom, bookTo, bookRate, rateType, bookDate) Values (" + request.form.get('memberInput') +"," + request.form.get('spaceInput')  + "," + request.form.get('startInput') + "," + request.form.get('endInput') + "," + request.form.get('rateInput') + "," + request.form.get('typeInput') + "," + datetime.now() + ")"
  bookingID = commit_booking_to_db(query)
  query = "insert into ledger (entryDate, bookingID, entryType, entryDesc, entryValue) values (" + datetime.now() + "," + bookingID + "," + ", 'SECURITY','Security Deposit'," + request.form.get('securityInput')
  result = commit_ledger_to_db(query)
  query = "insert into ledger (entryDate, bookingID, entryType, entryDesc, entryValue) values (" + datetime.now() + "," + bookingID + "," + ", 'ADVANCE','Advance Deposit'," + request.form.get('advanceInput')
  result = commit_ledger_to_db(query)
  query = "update spaces set isempty ='No' where ID = " + request.form.get('spaceInput')
  result = commit_space_to_db(query)
  return redirect("/spaces")
  
  

@app.route("/invoicing")
def show_invoices():
  return render_template("invoicing.html", title="Invoicing")

@app.route("/reporting")
def show_reporting():
  return render_template("reporting.html", title="Reporting")


print(__name__)
if __name__ == "__main__" :
  app.run(host="0.0.0.0", debug=True)
