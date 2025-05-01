import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

sqluser = os.getenv('user')
sqlpassword = os.getenv('password')

mysql1 = mysql.connector.connect(host="localhost", user= sqluser , password=sqlpassword, use_pure= True)
print(mysql1)