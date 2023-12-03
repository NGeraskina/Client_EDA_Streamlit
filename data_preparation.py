import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine


# Load .env file
load_dotenv()

host_db = os.getenv('HOST_DB')
user_db = os.getenv('USER_DB')
pswd_db = os.getenv('PSWD_DB')
name_db = os.getenv('NAME_DB')
print(host_db, user_db, pswd_db, name_db)

# Connect to the Postgres database
# conn = psycopg2.connect(connection_string)
conn = psycopg2.connect(host=host_db, user=user_db, password=pswd_db, dbname=name_db)
# Create a cursor object
cur = conn.cursor()

# Execute SQL commands to retrieve the current time and version from PostgreSQL
cur.execute('SELECT * FROM CLIENTS;')
row = cur.fetchone()
print(row)

cur.close()
conn.close()