import mysql.connector

mysql1 = mysql.connector.connect(host="localhost", user="root", password='mysql123', use_pure= True)
print(mysql1)