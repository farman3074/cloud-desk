from sqlalchemy import create_engine,text

db_connection_str = "mysql+pymysql://2fzl6ju8u6hjdoucny2v:pscale_pw_FIiZ7VQBVBzSwoKYp1XcQin2rFek3g8cQxKB5YCXJqK@ap-south.connect.psdb.cloud/clouddesk?charset=utf8mb4"


engine = create_engine(db_connection_str,connect_args={"ssl":{"ssl_ca": "/etc/ssl/cert.pem"}})

