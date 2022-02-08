import mysql.connector
import json
from flask import Flask
from time import time
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, Docker!'
  

@app.route('/widgets')
def get_widgets():
  try:
    mydb = mysql.connector.connect(
      #host="20.113.12.34",
      host="mysql",
      user="mysql_bart",
      password="passwd",
      database="inzynier"
    )
  except:
    print("Pierwsze polaczenie")
  cursor = mydb.cursor()


  cursor.execute("SELECT * FROM widgets")

  row_headers=[x[0] for x in cursor.description] #this will extract row headers

  results = cursor.fetchall()
  json_data=[]
  for result in results:
    json_data.append(dict(zip(row_headers,result)))

  cursor.close()

  return json.dumps(json_data)

@app.route('/initdb')
def db_init():

  try:
    mydb = mysql.connector.connect(
      #host="20.113.12.34",
      host="mysql",
      user="mysql_bart",
      password="passwd",
      database="inzynier"
    )
  except:
    print("Trzecie polaczenie")
  cursor = mydb.cursor()

  

  cursor.execute("DROP TABLE IF EXISTS widgets")
  #cursor.execute("CREATE TABLE widgets (id int ,name VARCHAR(255), description VARCHAR(255))")
  cursor.execute("CREATE TABLE widgets (id int NOT NULL AUTO_INCREMENT PRIMARY KEY ,name VARCHAR(255), description VARCHAR(255),z int)")
   
  c =0
  while c <= 30000:
    
    sql = "INSERT INTO widgets ( name, description, z) VALUES ( %s, %s, %s)"
    val = ("Johna", "Highwaya",((c+1)*2)-1)
    cursor.execute(sql, val)
    c=c+1
  

  mydb.commit()
  cursor.close()

  return 'init database'

@app.route('/selectdb')
def db_select():
  try:
    mydb = mysql.connector.connect(
      #host="20.113.12.34",
      host="mysql",
      user="mysql_bart",
      password="passwd",
      database="inzynier"
    )
  except:
    print("Trzecie polaczenie")
  cursor = mydb.cursor(buffered=True)
  #cursor = mydb.cursor()
  c =1
  while c <= 30000:
    #sql = "SELECT * FROM widgets where id > Val2 = '%d' *10 and id < (Val3 = '%d' +1)*10 " % (c,c)
    sql = """SELECT * FROM widgets WHERE id >  %s AND id <(%s +1)*10 LIMIT 0, 1"""
    tuple1 = (c,c)
    cursor.execute(sql,tuple1)
    c=c+1
  
  cursor.close()

if __name__ == "__main__":
  app.run(host ='0.0.0.0')