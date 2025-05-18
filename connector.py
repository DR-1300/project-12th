import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

sqluser = os.getenv('user')
sqlpassword = os.getenv('password')

mysql1 = mysql.connector.connect(host="localhost", user= sqluser , password=sqlpassword, use_pure= True, database="parking")
c = mysql1.cursor()
c.execute("show tables")
tables = c.fetchall()
for table in tables:
    if table[0] != "parking":
        continue
    else:
        c.execute("select * from parking")
        rows = c.fetchall()
        if len(rows) == 0:
            print("No data in the parking table.")
c.close()