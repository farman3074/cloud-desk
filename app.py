from flask import Flask,render_template,request,redirect,flash
#import datafile
from datetime import datetime
from database import load_members_from_db,load_member_from_db, commit_member_to_db, load_spaces_from_db, load_space_from_db, commit_space_to_db, commit_booking_to_db,commit_query_to_db,load_bookings_from_db,commit_invoice_to_db,load_invoices_from_db,load_invoiceLI_from_db,load_invoice_from_db,load_active_members_from_db,creat_monthly_invoice,commit_ledger_to_db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from flask_login import login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#app.SQLALCHEMY_DATABASE_URI = os.environ['DB_CONNECT_STR']

#PRODUCTION
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
#DEVELOPMENT
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI_DEV']


db = SQLAlchemy()
db.init_app(app)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
  userName = db.Column(db.String(45))  
  userPWD = db.Column(db.String(45))
  userGroup = db.Column(db.String(45))
  userEmail = db.Column(db.String(45), unique=True)
  

login_manager = LoginManager()
login_manager.login_view = ''
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/logincheck",methods =["POST"])
def check_login():
  #error = None
  email = request.form.get('username')
  pwd = request.form.get('pswrd')
  remember = True if request.form.get('remember') else False
  #app.logger.info(email)
  #user = User.query.filter_by(userEmail=email).first()
  user = User.query.filter_by(userEmail=email).first()

  # if the user doesn't exist or password is wrong, reload the page
  if not user or user.userPWD != pwd:
    flash('Please check your login details and try again.')
    return redirect("/") 
  
  login_user(user, remember=remember)
  return redirect("/dashboard")
  

@app.route("/dashboard")
@login_required
def show_dashbaord():
  return render_template("dashboard.html", title="Dash Board", userName=current_user.userEmail, userGroup = current_user.userGroup)

@app.route("/members")
@login_required
def show_members():
  members = load_members_from_db()
  return render_template("members.html", title="Members", members=members, userName=current_user.userEmail, userGroup = current_user.userGroup)

@app.route("/viewmember/<id>")
@login_required
def show_member(id):
  member = load_member_from_db(id)
  return render_template("viewmember.html", title="View Member",member=member)

@app.route("/editmember/<id>")
@login_required
def edit_member(id):
  member = load_member_from_db(id)
  return render_template("editmember.html", title="Edit Member",member=member)

@app.route("/commitmember",methods =["POST"])
@login_required
def commit_member():
  query = "update members set name ='" + request.form.get('nameInput') + "', company = '" + request.form.get('companyInput') + "', email ='" + request.form.get('emailInput') + "', phone = '" +  request.form.get('phoneInput') + "', nature = '" + request.form.get('natureInput') + "', address = '" + request.form.get('addressInput') + "' where ID= " + request.form.get('idInput')
  result = commit_member_to_db(query)
  return redirect(f"/viewmember/{request.form.get('idInput')}")

@app.route("/addmember")
@login_required
def add_member():
  return render_template("addmember.html", title="Add Member")

@app.route("/commitaddmember",methods =["POST"])
@login_required
def commit_add_member():
  query = "insert into members (`name`, `company`, `email`, `phone`, `nature`, `address`, `membership_date`) VALUES ('" + request.form.get('nameInput') + "', '" + request.form.get('companyInput') + "','" + request.form.get('emailInput') + "','" +  request.form.get('phoneInput') + "','" + request.form.get('natureInput') + "','" + request.form.get('addressInput') + "','" + datetime.now().strftime("%Y-%m-%d") + "')" 
  result = commit_member_to_db(query)
  return redirect("/members")

  
@app.route("/spaces")
@login_required
def show_spaces():
  spaces = load_spaces_from_db()
  return render_template("spaces.html", title="Spaces", spaces=spaces,userName=current_user.userEmail, userGroup = current_user.userGroup)

@app.route("/viewspace/<id>")
@login_required
def show_space(id):
  space = load_space_from_db(id)
  bookings = load_bookings_from_db(id)
  return render_template("viewspace.html", title="View Space",space=space, bookings=bookings)

@app.route("/editspace/<id>")
@login_required
def edit_space(id):
  space = load_space_from_db(id)
  return render_template("editspace.html", title="Edit space",space=space)

@app.route("/addspace")
@login_required
def add_space():
  return render_template("addspace.html", title="Add Space")

@app.route("/commitspace",methods =["POST"])
def commit_space():
  query = "update spaces set name ='" + request.form.get('nameInput') + "', type = '" + request.form.get('typeInput') + "', floor ='" + request.form.get('floorInput') + "', seats = " +  request.form.get('seatsInput') + ", area = " + request.form.get('areaInput') + ", isempty = '" + request.form.get('emptyInput') + "', listRate = '"+ request.form.get('rateInput') +"', rateType = '"+ request.form.get('ratetypeInput') +"' where ID= " + request.form.get('idInput')
  result = commit_space_to_db(query)
  return redirect(f"/viewspace/{request.form.get('idInput')}")

@app.route("/commitaddspace",methods =["POST"])
@login_required
def commit_add_space():
  query = "insert into spaces(`name`, `floor`, `seats`, `area`, `type`, `isempty`, `listRate`, `rateType`) VALUES ('" + request.form.get('nameInput') + "','" + request.form.get('floorInput') + "','" +  request.form.get('seatsInput') + "','" + request.form.get('areaInput') + "','" + request.form.get('typeInput') + "','Yes','" + request.form.get('rateInput') + "','" + request.form.get('ratetypeInput') + "')"
  result = commit_space_to_db(query)
  return redirect("/spaces")


@app.route("/bookspace/<id>")
@login_required
def book_space(id):
  space = load_space_from_db(id)
  members = load_members_from_db()
  currentdate = datetime.now().date()
  return render_template("bookspace.html", title = "Book " + space['name'], space=space, members=members, currentdate = currentdate)

@app.route("/commitbooking",methods =["POST"])
@login_required
def commit_booking():
  query = "insert into bookings (memberID, spaceID, bookFrom, bookTo, bookRate, rateType, bookDate) Values (" + request.form.get('memberInput') +"," + request.form.get('spaceInput')  + ",'" + request.form.get('startInput') + "','" + request.form.get('endInput') + "'," + request.form.get('rateInput') + ",'" + request.form.get('ratetypeInput') + "','" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "')"
  bookingID = commit_booking_to_db(query)
#  query = "insert into ledger (entryDate, bookingID, entryType, entryDesc, entryValue) values ('" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "'," + str(bookingID['ID']) + ", 'SECURITY','Security Deposit'," + request.form.get('securityInput')+")"
  #create advance and security invoices only when spaceType is not 'Resource'
  if request.form.get('spaceType') != "Resource":
    invAmt = int(request.form.get('securityInput')) + int( request.form.get('advanceInput'))
    query = "insert into invoices (createdon,invoicedate,duedate,memberID,header,footer,invoiceamt,amtwithtax,invoicetype) values ('" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "','" + datetime.now().strftime("%Y-%m-%d") + "','" + datetime.now().strftime("%Y-%m-%d") + "'," + request.form.get('memberInput') + ",'Invoice for Security and Advance','Please pay by cheque or bank transfer to A/C # XXXXXX'," + str(invAmt) + ","+ str(invAmt) +",'SECURITYADVANCE')"
    invoiceID = commit_invoice_to_db(query)
    query = "insert into invoiceLI (invoiceID,itemNum,itemDesc,itemRate,itemqty,itemtotal,bookingID) values ('" + str(invoiceID['ID']) + "',1,'Security Deposit',0,1," + request.form.get('securityInput') + ",'" + str(bookingID['ID']) + "')"
    result = commit_query_to_db(query)
    query = "insert into invoiceLI (invoiceID,itemNum,itemDesc,itemRate,itemqty,itemtotal,bookingID) values ('" + str(invoiceID['ID']) + "',2,'Advance Rent',0,1," + request.form.get('advanceInput') + ",'" + str(bookingID['ID']) + "')"
    result = commit_query_to_db(query)
  #query = "insert into ledger (entryDate, bookingID, entryType, entryDesc, entryValue) values ('" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "'," + str(bookingID['ID']) + ", 'ADVANCE','Advance Deposit'," + request.form.get('advanceInput') +")"
    #end if here
  
  query = "update spaces set isempty ='No' where ID = " + request.form.get('spaceInput')
  result = commit_space_to_db(query)
  return redirect("/spaces")
  #return request.form.get('ratetypeInput')
  
@app.route("/invoicing")
@login_required
def show_invoices():
  invoices = load_invoices_from_db()
  query = "SELECT ID,name FROM members where members.ID in (select memberID from bookings where bookings.bookto > '"+ datetime.now().strftime("%Y-%m-%d") + "')"
  result = load_active_members_from_db(query)
  currentdate = datetime.now().date()
  return render_template("invoicing.html", title="Invoicing", invoices=invoices, members = result, currentdate = currentdate, userName=current_user.userEmail, userGroup = current_user.userGroup)

@app.route("/viewinvoice/<id>")
@login_required
def show_invoice(id):
  invoice = load_invoice_from_db(id)
  member = load_member_from_db(invoice['memberID'])
  invoiceLIs = load_invoiceLI_from_db(id)
  return render_template("viewinvoice.html", title="Customer Invoice", invoice=invoice,member=member,invoiceLI=invoiceLIs)

# this one is replaced by a Modal now
@app.route("/payinvoice/<id>")
@login_required
def pay_invoice(id):
  return render_template("payinvoice.html", invoiceID=id)

@app.route("/commitpayment",methods =["POST"])
@login_required
def commit_invoice():
  query = "Update invoices set ispaid = 'Y', instrumentType ='" + request.form.get('instrumentType') +"',instrumentRef='" + request.form.get('instrumentRef') +"',paydate='" +request.form.get('instrumentDate') +"',paidamt =" +request.form.get('amount') +" where ID = " + request.form.get('invoiceID')
  result = commit_query_to_db(query)
  query = "insert into ledger (entryDate, entryRef, entryType, entryDesc, entryValue) values ('" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "'," + request.form.get('invoiceID') + ",'INVOICE', 'Invoice Payment by Customer'," + request.form.get('amount') + ")"
  result = commit_query_to_db(query)
  return redirect(f"/viewinvoice/{request.form.get('invoiceID')}")

@app.route("/newinvoice",methods =["POST"])
@login_required
def new_invoice():
  if request.form.get("memberInput") == "0":
    query = "SELECT ID,name FROM members where members.ID in (select memberID from bookings where bookings.bookto > '"+ datetime.now().strftime("%Y-%m-%d") + "')"
    results = load_active_members_from_db(query)

    for result in results:
      creat_monthly_invoice(request.form.get("fromInput"),request.form.get("toInput"), result.get("ID"))       
  else:
    creat_monthly_invoice(request.form.get("fromInput"),request.form.get("toInput"),request.form.get("memberInput"))
  
    
  return redirect("/invoicing")
   

@app.route("/reporting")
@login_required
def show_reporting():
  currentDate = datetime.now()
  currentMonth = str(currentDate.year) + "-" + str(currentDate.month)
  return render_template("reporting.html", title="Reporting", userName=current_user.userEmail, userGroup = current_user.userGroup, currentMonth = currentMonth)

@app.route("/backoffice")
@login_required
def show_accounting():
#  return render_template("accounting.html", title="Back Office", userName=current_user.userEmail, userGroup = current_user.userGroup)
  return render_template("testheader.html", title="Dash Board", userName=current_user.userEmail, userGroup = current_user.userGroup)

@app.route("/ledger")
@login_required
def new_ledger():
  return render_template("ledger.html", title="Ledger Entry", userName=current_user.userEmail, userGroup = current_user.userGroup)


@app.route("/pettycash")
@login_required
def new_petty():
  return render_template("pettycash.html", title="Petty Cash Entry", userName=current_user.userEmail, userGroup = current_user.userGroup)

@app.route("/commitledger",methods =["POST"])
@login_required
def commit_ledger():

  amount = int(request.form.get("amount"))
  description = request.form.get("instrumentRef") + "-" + request.form.get("instrumentDate") + "-" + request.form.get("desc")
  entryType = request.form.get("entryType")
  
  if entryType != "InvDeposit" or entryType != "ODeposit":
    amount = amount * -1
  
  query = "insert into ledger (entryDate,entryRef,entryType,entryDesc,entryValue) values ('" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "',0,'" + entryType + "','" + description + "'," + str(amount) + ")"
  
  ledgerID = commit_ledger_to_db(query)
  
  # update petty cash register for Petty Cash withdrawls
  if entryType == "Petty":
    query = "insert into pettycash (entryDate,entryDesc,entryValue,entryRef) values ('" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "','Petty Cash addition'," + str(amount * -1) + ",'" + str(ledgerID['ID']) + "')"
    result = commit_query_to_db(query)

  flash('Entry posted in ledger')
  return redirect("/ledger")

@app.route("/commitpetty",methods =["POST"])
@login_required
def commit_petty():
  amount = int(request.form.get("amount"))
  query = "insert into pettycash (entryDate,entryDesc,entryValue,entryRef,entryHead) values ('" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "','"+ request.form.get("desc") +"'," + str(amount * -1) + ",0,'" + request.form.get("expHead") + "')"
  result = commit_query_to_db(query)
  flash('Entry posted in Petty Cash Register')
  return redirect("/pettycash")

@app.route("/extras")
@login_required
def new_extras():
  members = load_members_from_db()
  return render_template("extras.html", title="Extras Entry",members=members, userName=current_user.userEmail, userGroup = current_user.userGroup)

@app.route("/commitextras",methods=["POST"])
@login_required
def commit_extras():
  query = "insert into extras (entryDate,memberID,extrasDesc,fromDate,toDate,amount,extrasNotes) values ('"+ datetime.now().strftime("%Y-%m-%d") + "'," + request.form.get("memberID") + ",'" + request.form.get("extrasDesc") + "','" + request.form.get("fromDate") + "','" + request.form.get("toDate") + "'," + str(request.form.get("amount")) + ",'" + request.form.get("notes") + "')"
  result = commit_query_to_db(query)
  flash('Entry posted in Extras Register')
  return redirect("/extras")
  

@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect("/")


print(__name__)
if __name__ == "__main__" :
  app.run(host="0.0.0.0", debug=True)
