# from flask import Flask
from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd
import time
import pickle
import redis
import random

app = Flask(__name__)
r = redis.StrictRedis(host="swatiredis.redis.cache.windows.net", port=6380,password="4G67nLQxPEzXJBu0Gh1wcNgZcBbvAnLw4YqAGdb2aEQ=",ssl=True)

@app.route('/')
def index():
    r.set("swathi",1)
    return render_template('index.html')

@app.route('/display')
def display():
    return render_template('display.html')

@app.route('/enternew')
def upload_csv():
    return render_template('upload.html')

@app.route('/list')
def list():
    cache = "mycache"
    start_t = time.time()
    query = "select * from Earthquake"
    if r.get(cache):
        t = "with"
        print(t)
        isCache = 'with Cache'

        rows = pickle.loads(r.get(cache))
        r.delete(cache)

    else:
        t = "without"
        print(t)
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        con.close()
        r.set(cache, pickle.dumps(rows))
    end_t = time.time() - start_t
    print(end_t)
    return render_template("table.html", rows=t, stime=end_t)

@app.route('/select')
def select():
    for i in range(100):
        cache = "mycache"
        start_t = time.time()
        var=str(random.uniform(2, 5))
        query = "select * from Earthquake where mag > " +var
        if r.get(cache+str(i)):
            t = "with"
            print(t)
            isCache = 'with Cache'

            rows = pickle.loads(r.get(cache+str(i)))
            #r.delete(cache)

        else:
            t = "without"
            print(t)
            con = sql.connect("database.db")
            cur = con.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            con.close()
            r.set(cache+str(i), pickle.dumps(rows))
        end_t = time.time() - start_t
        print(end_t)
        return render_template("table.html", rows=t, stime=end_t)

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
