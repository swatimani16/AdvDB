# from flask import Flask
from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enternew')
def upload_csv():
    return render_template('upload.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
       con = sql.connect("database.db")
       csv = request.files['myfile']
       file = pd.read_csv(csv)
       file.to_sql('Earthquake', con, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)
       con.close()
       return render_template("result.html",msg = "Record inserted successfully")

if __name__ == '__main__':
  app.run()
