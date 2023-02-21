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

def commit_member_to_db(form):
  with engine.connect() as conn:
    query = f"update members set name = {form['nameInput']}, company = {form['companyInput']}, email = {form['emailInput']}, phone =  {form.get('phoneInput')}, nature = {form.get('natureInput')}, address = {form.get('addressInput')} where ID= {form.get('idInput')}"
    result = conn.execute(text(query))
    return result
    
    
    