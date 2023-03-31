from sqlalchemy import create_engine,text
import calendar
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
  currMonth = datetime.strptime(startdate,"%Y-%m-%d").month
  currYear = datetime.strptime(startdate,"%Y-%m-%d").year
  firstDayDate = datetime.datetime(currYear, currMonth, 1)
  numDays = calendar.monthrange(currYear,currMonth)
  lastDayDate = datetime.datetime(currYear, currMonth, numDays)
  
  query = "Select * from bookings where memberID = '" + memberid + "' and bookings.bookFrom <= '" + firstDayDate + "' and bookings.bookto >= '" + lastDayDate + "'"
  with engine.connect() as conn:
    results = conn.execute(text(query))
    for result in results:
        
  return