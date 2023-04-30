from sqlalchemy import create_engine,text
import calendar
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
import os

#PRODUCTION
#db_connection_str = os.environ['DB_CONNECT_STR']
#DEVELOPMENT
db_connection_str = os.environ['DB_CONNECT_STR_DEV']

engine = create_engine(db_connection_str,connect_args={"ssl":{"ssl_ca": "/etc/ssl/cert.pem"}})


def update_db_lastlogin(user):
  with engine.connect() as conn:
    query = "update user set lastLogin = '" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "' where id = " + str(user.id)
    result = conn.execute(text(query))
    return result

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

def commit_ledger_to_db(query):
  with engine.connect() as conn:
    result = conn.execute(text(query))
    result = conn.execute(text("select ID from ledger ORDER BY ID DESC LIMIT 1"))
    rows = result.all()
    return rows[0]._mapping

def load_results_from_db(query):
  with engine.connect() as conn:
    result = conn.execute(text(query))
    rows = result.all()
    results = []
    for row in rows:
      results.append(row._mapping)
    return results
    
    
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

def load_bookings_bymember_from_db(id):
  with engine.connect() as conn:
    query = f"SELECT * FROM clouddesk.bookings, clouddesk.spaces where  bookings.memberID = { id } and clouddesk.bookings.spaceID = clouddesk.spaces.ID"
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


def load_tickets_from_db():
  with engine.connect() as conn:
   # result = conn.execute(text("select tickets.*,members.name from tickets,members where members.ID = tickets.memberID))
    result = conn.execute(text("select tickets.*,members.name from tickets LEFT JOIN members on tickets.memberID = members.ID"))
    tick_list = result.all()
    tickets = []
    for row in tick_list:
      tickets.append(row._mapping)
    return tickets

def load_ticket_from_db(id):
  with engine.connect() as conn:
  #  query = f"select tickets.*,members.name from tickets,members where tickets.ID = {id} and members.ID = tickets.memberID"
    query = f"select tickets.*,members.name from tickets LEFT JOIN members on tickets.memberID = members.ID where tickets.ID = {id} "
    result = conn.execute(text(query))
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return rows[0]._mapping
  
def load_active_members_from_db(query):
  with engine.connect() as conn:
    result = conn.execute(text(query))
    mem_list = result.all()
    members = []
    for row in mem_list:
      members.append(row._mapping)
    return members

def get_opening_bal(table,period):
  #startdate = datetime.strptime(period, '%Y-%m')
  startdate = period.split("-")
  currMonth = int(startdate[1])
  currYear = int(startdate[0])
  firstDayDate = date(currYear, currMonth, 1)
  #print(currMonth)
  with engine.connect() as conn:
    query = "select sum(entryValue) as balance from " + table + " where entryDate < '" + firstDayDate.strftime("%Y-%m-%d") + "'"
    result = conn.execute(text(query))
    rows = result.all()
    if len(rows) == 0:
      return 0
    else:
      result = rows[0]._mapping
      balance = result['balance']
      if balance == None:
        balance = 0
      return balance

def get_entries_from_db(table,period):
  #startdate = datetime.strptime(period, '%Y-%m')
  #currMonth = startdate.month
  #currYear = startdate.year
  startdate = period.split("-")
  currMonth = int(startdate[1])
  currYear = int(startdate[0])
  firstDayDate = datetime(currYear, currMonth, 1)
  monthCal = calendar.monthrange(currYear,currMonth)
  numDays = monthCal[1]
  lastDayDate = datetime(currYear, currMonth, numDays)
  with engine.connect() as conn:
    query = "select * from " + table + " where entryDate >= '" + firstDayDate.strftime("%Y-%m-%d") + "' and entryDate <= '" + lastDayDate.strftime("%Y-%m-%d 23:59:59") + "' order by entryDate"
    result = conn.execute(text(query))
    rows = result.all()
    entries = []
    for row in rows:
      entries.append(row._mapping)
    return entries


def load_staffs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from user"))
    staff_list = result.all()
    staffs = []
    for row in staff_list:
      staffs.append(row._mapping)
    return staffs
  
def creat_monthly_invoice(startdate,enddate, memberid):
  
  startdate = datetime.strptime(startdate, '%Y-%m-%d')
  currMonth = startdate.month
  currYear = startdate.year
  firstDayDate = date(currYear, currMonth, 1)
  monthCal = calendar.monthrange(currYear,currMonth)
  numDays = monthCal[1]
  lastDayDate = date(currYear, currMonth, numDays)

  lastMonthStart = firstDayDate - relativedelta(months=1)
  
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


      # ORIGINAL - covered full months only
      #query = "Select bookings.*,spaces.name from bookings,spaces where memberID = '" + str(memberid) + "' and bookings.bookFrom <= '" + firstDayDate.strftime("%Y-%m-%d") + "' and bookings.bookto >= '" + lastDayDate.strftime("%Y-%m-%d") + "' and bookings.spaceID = spaces.ID"

      #MODIFIED to cover partial months also
      query = "Select bookings.*,spaces.name,spaces.type from bookings,spaces where memberID = '" + str(memberid) + "' and ((spaces.type != 'Resource' and bookings.bookFrom <= '" + firstDayDate.strftime("%Y-%m-%d") + "' and bookings.bookTo >= '" + firstDayDate.strftime("%Y-%m-%d") + "') or (spaces.type = 'Resource' and bookings.bookFrom >= '" + lastMonthStart.strftime("%Y-%m-%d") + "' and bookings.bookTo < '" + firstDayDate.strftime("%Y-%m-%d") + "')) and bookings.spaceID = spaces.ID"

#      query = "Select * from bookings where memberID = '" + str(memberid) + "' and bookings.bookFrom <= '" + firstDayDate.strftime("%Y-%m-%d") + "' and bookings.bookto >= '" + lastDayDate.strftime("%Y-%m-%d") + "'"


#      query = "Select * from bookings where memberID = '" + str(memberid) + "' and bookings.bookFrom <= '" + firstDayDate.strftime("%Y-%m-%d") + "' and bookings.bookto >= '" + lastDayDate.strftime("%Y-%m-%d") + "'"

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
        counter = 1
        for row in bookings:
  
          if row['type'] != "Resource":
            # Check for partial months and first months post booking (partial invoicing)
            billDays = numDays 
            firstDayDate = date(currYear, currMonth, 1)
            lastDayDate = date(currYear, currMonth, numDays)
          
            bookFrom = row['bookFrom']
            bookMonth = bookFrom.month
            bookYear = bookFrom.year
            bookDay = bookFrom.day
            numDaysLast = numDays

            bookTo = row['bookTo']
            toMonth = bookTo.month
            toYear = bookTo.year
            toDay = bookTo.day
          
          
            if (bookYear == currYear and bookMonth == currMonth - 1) or (bookMonth == 12 and currMonth == 1 and bookYear == currYear-1):
              # booking was done last month of the same year or decoember of last year (and we are invoicing in Jan)

              numDaysLast = (calendar.monthrange(bookYear,bookMonth))[1]
              billDays = numDaysLast - bookDay + 1
              firstDayDate = bookFrom
              lastDayDate = date(bookYear,bookMonth,numDaysLast)
            
          
            if toYear == currYear and toMonth == currMonth:
              # booking expiring in the current month - so partial billing
              numDaysLast = numDays
              billDays = toDay
              firstDayDate = date(currYear, currMonth, 1)
              lastDayDate = date(toYear,toMonth,toDay)
          
            if row['rateType'] == "MONTHLY":
              rental = (row['bookRate'] / numDaysLast) * billDays
            if row['rateType'] == "WEEKLY":
              rental = (row['bookRate'] / 7) * billDays
            if row['rateType'] == "HOURLY":
              rental = row['bookRate'] * 24 * billDays
            if row['rateType'] == "DAILY":
              rental = row['bookRate'] * billDays
    
            query = "insert into invoiceLI (invoiceID,itemNum,itemDesc,itemRate,itemqty,itemtotal,bookingID) values (" + str(invoiceID['ID']) + ","+str(counter)+",'Monthly Rental for "+ str(row['name']) +"- "+ firstDayDate.strftime("%Y-%m-%d") +" to " + lastDayDate.strftime("%Y-%m-%d") + "',"+ str(row['bookRate']) +",1," + str(rental) + "," + str(row['ID']) + ")"


    
        #    if row['rateType'] == "MONTHLY":
        #      rental = row['bookRate']
        #    if row['rateType'] == "WEEKLY":
        #      rental = row['bookRate'] * 4
        #    if row['rateType'] == "HOURLY":
        #      rental = row['bookRate'] * 24 * numDays
        #    if row['rateType'] == "DAILY":
        #      rental = row['bookRate'] * numDays
    
        #   query = "insert into invoiceLI (invoiceID,itemNum,itemDesc,itemRate,itemqty,itemtotal,bookingID) values (" + str(invoiceID['ID']) + ","+str(counter)+",'Monthly Rental for "+ str(row['spaceID']) +"',0,1," + str(rental) + "," + str(row['ID']) + ")"

          else:
            # deal cases for "Resource"
            bookFrom = row['bookFrom']
            bookTo = row['bookTo']
            duration = bookTo - bookFrom
            billHours = duration.total_seconds() / 3600
            rental = row['bookRate'] * billHours

            query = "insert into invoiceLI (invoiceID,itemNum,itemDesc,itemRate,itemqty,itemtotal,bookingID) values (" + str(invoiceID['ID']) + ","+str(counter)+",'Resource Rental for "+ str(row['name']) +"- "+ bookFrom.strftime("%Y-%m-%d %H:%M:%S") +" to " + bookTo.strftime("%Y-%m-%d %H:%M:%S") + "',"+ str(row['bookRate']) + ","+ str(billHours) + "," + str(rental) + "," + str(row['ID']) + ")"

          result = commit_query_to_db(query)

          invAmt = invAmt + rental
          counter = counter + 1

        # find extras for this members if any and add line items
        # invoiceID = 0 means it is not included in any invoice
        query = "Select * from extras where memberID = '" + str(memberid) + "' and invoiceID = '0' and fromDate >= '" + lastMonthStart.strftime("%Y-%m-%d") + "'"
        results = conn.execute(text(query))
        extras_list = results.all()
        extras = []
        for row in extras_list:
          extras.append(row._mapping)
        if len(extras) > 0:
          for row in extras:
            rental = row['amount']
            query = "insert into invoiceLI (invoiceID,itemNum,itemDesc,itemRate,itemqty,itemtotal,bookingID) values (" + str(invoiceID['ID']) + ","+str(counter)+",'"+ row['extrasDesc'] +"- "+ row['fromDate'].strftime("%Y-%m-%d") +" to " + row['toDate'].strftime("%Y-%m-%d") + "',"+ str(rental) + ",1," + str(rental) + "," + str(row['ID']) + ")"

            result = commit_query_to_db(query)
            invAmt = invAmt + rental
            counter = counter + 1

            # update extras line entry with the attached invoice ID
            query = "update extras set invoiceID = "+ str(invoiceID['ID']) + " where ID = "+ str(row['ID'])
            
            result = commit_query_to_db(query)
          # extras code ends here
        
        # now update amounts in the invoice table
        query = "update invoices set invoiceamt = " + str(invAmt) + ",taxamount = 0, amtwithtax = " + str(invAmt) + ", discount = 0 where ID = " + str(invoiceID['ID'])
        result = commit_query_to_db(query)

  return 0