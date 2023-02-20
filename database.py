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
