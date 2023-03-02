from sqlalchemy import create_engine,text
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
    return result['ID']

def commit_ledger_to_db(query):
  with engine.connect() as conn:
    result = conn.execute(text(query))
    return result
  