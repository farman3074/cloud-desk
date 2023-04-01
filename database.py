from sqlalchemy import create_engine,text
import calendar
from datetime import datetime,date
import os

db_connection_str = os.environ['DB_CONNECT_STR']


engine = create_engine(db_connection_str,connect_args={"ssl":{"ssl_ca": "/etc/ssl/cert.pem"}})

def load_members_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from members"))
    mem_list = result.all()
    members = []
    for row in mem_list:
      members.append(row._mapping)
    return members

def load_member_from_db(id):
  with engine.connect() as conn:
    query = f"select * from members where ID = {id}"
    result = conn.execute(text(query))
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return rows[0]._mapping

def commit_member_to_db(query):
  with engine.connect() as conn:
    result = conn.execute(text(query))
    return result
    
    
def load_spaces_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from spaces"))
    mem_list = result.all()
    spaces = []
    for row in mem_list:
      spaces.append(row._mapping)
    return spaces
    
def load_space_from_db(id):
  with engine.connect() as conn:
    query = f"select * from spaces where ID = {id}"
    result = conn.execute(text(query))
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return rows[0]._mapping

def commit_space_to_db(query):
  with engine.connect() as conn:
    result = conn.execute(text(query))
    return result

def commit_booking_to_db(query):
  with engine.connect() as conn:
    result = conn.execute(text(query))
    result = conn.execute(text("select ID from bookings ORDER BY ID DESC LIMIT 1"))
    rows = result.all()
    return rows[0]._mapping

def commit_invoice_to_db(query):
  with engine.connect() as conn:
    result = conn.execute(text(query))
    result = conn.execute(text("select ID from invoices ORDER BY ID DESC LIMIT 1"))
    rows = result.all()
    return rows[0]._mapping
  
def commit_query_to_db(query):
  with engine.connect() as conn:
    result = conn.execute(text(query))
    return result

def load_bookings_from_db(id):
  with engine.connect() as conn:
    query = f"SELECT bookDate, bookFrom, bookTo, bookRate, rateType, members.name FROM clouddesk.bookings, clouddesk.members where spaceID = {id} and bookings.memberID = members.ID"
    result = conn.execute(text(query))
    rows = result.all()
    bookings = []
    for row in rows:
      bookings.append(row._mapping)
    return bookings
    
def load_invoices_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select invoices.ID,invoicedate,duedate,header,invoiceamt,taxamount,discount,amtwithtax,ispaid,members.name from invoices,members where invoices.memberID = members.ID"))
    inv_list = result.all()
    invoices = []
    for row in inv_list:
      invoices.append(row._mapping)
    return invoices

def load_invoice_from_db(id):
  with engine.connect() as conn:
    query = f"select * from invoices where ID = {id}"
    result = conn.execute(text(query))
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return rows[0]._mapping

def load_invoiceLI_from_db(id):
  with engine.connect() as conn:
    query = f"select * from invoiceLI where invoiceID = {id}"
    result = conn.execute(text(query))
    rows = result.all()
    LIs = []
    for row in rows:
      LIs.append(row._mapping)
    return LIs

def load_active_members_from_db(query):
  with engine.connect() as conn:
    result = conn.execute(text(query))
    mem_list = result.all()
    members = []
    for row in mem_list:
      members.append(row._mapping)
    return members

def creat_monthly_invoice(startdate,enddate, memberid):
  
  startdate = datetime.strptime(startdate, '%Y-%m-%d')
  currMonth = startdate.month
  currYear = startdate.year
  firstDayDate = date(currYear, currMonth, 1)
  monthCal = calendar.monthrange(currYear,currMonth)
  numDays = monthCal[1]
  lastDayDate = date(currYear, currMonth, numDays)

  with engine.connect() as conn:
    # first check if the invoice is already created
    query = "Select * from invoices where memberID = " + str(memberid) + " and invoicetype = 'MONTHLY" + str(currMonth) + str(currYear) + "'"
    results = conn.execute(text(query))
    result_list = results.all()
    invlist = []
    for row in result_list:
      invlist.append(row._mapping)
    if len(invlist) == 0:
      # select active bookings of this member
      query = "Select * from bookings where memberID = '" + str(memberid) + "' and bookings.bookFrom <= '" + firstDayDate.strftime("%Y-%m-%d") + "' and bookings.bookto >= '" + lastDayDate.strftime("%Y-%m-%d") + "'"
      results = conn.execute(text(query))
      book_list = results.all()
      bookings = []
      for row in book_list:
        bookings.append(row._mapping)
      if len(bookings) > 0:
        # create invoice for the current month
        query = "insert into invoices (createdon,invoicedate,duedate,memberID,header,footer,invoicetype) values ('" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "','" + datetime.now().strftime("%Y-%m-%d") + "','" + datetime.now().strftime("%Y-%m-%d") + "'," + str(memberid) + ",'Monthly Rental Invoice','Please pay by cheque or bank transfer to A/C # XXXXXX','MONTHLY"+ str(currMonth) + str(currYear) + "')"
        invoiceID = commit_invoice_to_db(query)
        # now create LIs against each booking
        invAmt = 0
        for row in bookings:
          counter = 1
    
          if row['rateType'] == "MONTHLY":
            rental = row['bookRate']
          if row['rateType'] == "WEEKLY":
            rental = row['bookRate'] * 4
          if row['rateType'] == "HOURLY":
            rental = row['bookRate'] * 24 * numDays
          if row['rateType'] == "DAILY":
            rental = row['bookRate'] * numDays
    
          query = "insert into invoiceLI (invoiceID,itemNum,itemDesc,itemRate,itemqty,itemtotal,bookingID) values (" + str(invoiceID['ID']) + ","+str(counter)+",'Monthly Rental for "+ str(row['spaceID']) +"',0,1," + str(rental) + "," + str(row['ID']) + ")"
          result = commit_query_to_db(query)

          invAmt = invAmt + rental
          counter = counter + 1

        # now update invoiceID in the invoice table
        query = "update invoices set invoiceamt = " + str(invAmt) + ",taxamount = 0, amtwithtax = " + str(invAmt) + ", discount = 0 where ID = " + str(invoiceID['ID'])
        result = commit_query_to_db(query)
  
  return 0