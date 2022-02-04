import mysql.connector
import json
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
  db_init()
  get_widgets()
  return 'Hello, Docker!'
  

@app.route('/widgets')
def get_widgets():
  try:
    mydb = mysql.connector.connect(
      host="mysql",
      user="root",
      password="root",
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
      host="mysql",
      user="root",
      password="root"
    )
  except:
    print("Drugie polaczenie")
  cursor = mydb.cursor()

  cursor.execute("DROP DATABASE IF EXISTS symfony_docker")
  cursor.execute("CREATE DATABASE symfony_docker")
  cursor.close()

  try:
    mydb = mysql.connector.connect(
      host="mysql",
      user="root",
      password="root",
      database="inzynier"
    )
  except:
    print("Trzecie polaczenie")
  cursor = mydb.cursor()

  

  cursor.execute("DROP TABLE IF EXISTS widgets")
  cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")

  sql = "INSERT INTO widgets (name, description) VALUES (%s, %s)"
  val = ("John", "Highway")
  cursor.execute(sql, val)

  cursor.close()

  return 'init database'

if __name__ == "__main__":
  app.run(host ='0.0.0.0')