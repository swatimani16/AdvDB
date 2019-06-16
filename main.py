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

@app.route('/formfill')
def formfill():
    return render_template('formfill.html')

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
        var=str(round(random.uniform(2, 5)))
        query = "select * from Earthquake where mag > " +var
        if r.get(cache+var):
            t = "with"
            print(t)
            isCache = 'with Cache'

            rows = pickle.loads(r.get(cache+var))
            #r.delete(cache)

        else:
            t = "without"
            print(t)
            con = sql.connect("database.db")
            cur = con.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            con.close()
            r.set(cache+var, pickle.dumps(rows))
        end_t = time.time() - start_t
        print(end_t)
        return render_template("table.html", rows=t, stime=end_t)


@app.route('/select_lat', methods=['GET', 'POST'])
def select_lat():
    #for i in range(100):
        cache = "mycache"
        start_t = time.time()
        if request.method =='POST':
            lat=request.form['lat1']
            lon=request.form['lon1']
            dist = request.form['dis']
            #var=str(random.uniform(2, 5))
            #query = "select * from Earthquake where lat < "+lat1+ and lat >+lat2
            query='SELECT * FROM (select *,(((acos(sin((' + lat + '*3.14/180)) * sin(("latitude"*3.14/180))+cos((' + lat + '*3.14/180))*cos(("latitude"*3.14/180))*cos(((' + lon + ' - "longitude")*3.14/180))))*180/3.14)*60*1.1515*1.609344) as distance from KDJ50223.EARTHQUAKE ) where distance <= ' + dist + ''
            if r.get(cache):
                t = "with"
                print(t)
                isCache = 'with Cache'

                rows = pickle.loads(r.get(cache))
                #r.delete(cache)

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

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   s_time=time.time()
   if request.method == 'POST':
       con = sql.connect("database.db")
       csv = request.files['myfile']
       file = pd.read_csv(csv)
       file.to_sql('Earthquake', con, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)
       con.close()
       e_time=time.time()-s_time
       return render_template("result.html",msg = "Record inserted successfully", time=e_time)

@app.route('/append_To_string',methods=['GET','POST'])
def append_To_string():
    query='select id from Earthquake where id LIKE "O%"'
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    s_time=time.time()
    val=random.randint(0,len(rows)-1)
    var=str(rows[val])
    query1="select * from earthquake where id ='"+var[2:12]+"'"
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(query1)
    rows1 = cur.fetchall()
    e_time=time.time()-s_time
    return render_template("result.html", msg=e_time)

@app.route('/append_cache',methods=['GET','POST'])
def append_cache():
        query = 'select id from Earthquake where id LIKE "O%"'
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        start_t = time.time()
        for i in range(100):
            cache = "mycache"
            val = random.randint(0, len(rows) - 1)
            var = str(rows[val])
            query1 = "select * from earthquake where id ='"+var[2:12]+"'"
            if r.get(cache+var):
                t = "with"
                print(t)
                isCache = 'with Cache'

                rows = pickle.loads(r.get(cache+var))
                #r.delete(cache)

            else:
                t = "without"
                print(t)
                con = sql.connect("database.db")
                cur = con.cursor()
                cur.execute(query1)
                rows1 = cur.fetchall()
                con.close()
                r.set(cache+var, pickle.dumps(rows))
        end_t = time.time() - start_t
        print(end_t)
        return render_template("table.html", rows=t, stime=end_t)

if __name__ == '__main__':
  app.run()
