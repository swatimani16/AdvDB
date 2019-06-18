# from flask import Flask
from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd
import time
import pickle
import redis
import random
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import math
from math import sqrt
app = Flask(__name__)
r = redis.StrictRedis(host="swatiredis.redis.cache.windows.net", port=6380,password="4G67nLQxPEzXJBu0Gh1wcNgZcBbvAnLw4YqAGdb2aEQ=",ssl=True)

#Index Page
@app.route('/')
def index():
    r.set("swati",1)
    return render_template('index.html')

#Clustering
@app.route('/clustering')
def clustering():
    return render_template('clustering.html')

#locationSource
@app.route('/location')
def location():
    return render_template('location.html')

#Select between two magnitudes
@app.route('/select_between')
def select_between():
    return render_template('select_between.html')

#Display greater than mag inputed
@app.route('/display')
def display():
    return render_template('display.html')

#Select between a pair of lat and lon and dates
@app.route('/select_between_dates')
def select_between_dates():
    return render_template('select_between_dates.html')

#Enter a csv file
@app.route('/enternew')
def upload_csv():
    return render_template('upload.html')

#Select between magnitude and less than a distance
@app.route('/formfill')
def formfill():
    return render_template('formfill.html')

#Delete the cache
@app.route('/delete_cache')
def delete_cache():
    return render_template('delete_cache.html')

#Enter the number of times you want the query to execute
@app.route('/select_count')
def select_count():
    return render_template('select_count.html')

#Display all the values of the database
@app.route('/list')
def list():
    cache = "mycache"
    start_t = time.time()
    query = "select * from Earthquake"
    if r.get(cache):
        t = "With Cache"
        print(t)
        isCache = 'with Cache'

        rows = pickle.loads(r.get(cache))
        r.delete(cache)

    else:
        t = "Without Cache"
        print(t)
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        con.close()
        r.set(cache, pickle.dumps(rows))
    end_t = time.time() - start_t
    print(end_t)
    return render_template("table_display.html",data=rows, rows=t, stime=end_t)

#Display all the values greater than value and take value of loop from the user
@app.route('/select',methods=['GET','POST'])
def select():
    if request.method=='POST':
        loop=int(request.form['loop'])
        for i in range(loop):
            cache = "mycache"
            start_t = time.time()
            var=str(round(random.uniform(2, 5)))
            query = "select * from Earthquake where mag > " +var
            if r.get(cache+var):
                t = "With Cache"
                print(t)
                isCache = 'with Cache'

                rows = pickle.loads(r.get(cache+var))
                #r.delete(cache)

            else:
                t = "Without Cache"
                print(t)
                con = sql.connect("database.db")
                cur = con.cursor()
                cur.execute(query)
                rows = cur.fetchall()
                con.close()
                r.set(cache+var, pickle.dumps(rows))
            end_t = time.time() - start_t
            print(end_t)
            return render_template("table_display.html",data=rows, rows=t, stime=end_t)


'''@app.route('/select_lat', methods=['GET', 'POST'])
def select_lat():
    #for i in range(100):
        cache = "mycache"
        start_t = time.time()
        if request.method =='POST':
            lat=float(request.form['lat1'])
            lon=float(request.form['lon1'])
            dist = request.form['dis']
            #var=str(random.uniform(2, 5))
            #query = "select * from Earthquake where lat < "+lat1+ and lat >+lat2
            a=str((((math.acos(math.sin((lat *3.14/180)) * math.sin(("latitude"*3.14/180))+math.cos((lat *3.14/180))*math.cos(("latitude"*3.14/180))*math.cos(((lon - "longitude")*3.14/180))))*180/3.14)*60*1.1515*1.609344))
            query='SELECT * FROM (select *,'+a+' as distance from Earthquake ) where distance <= ' + dist + ''
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
            return render_template("table.html",rows=t, stime=end_t)'''

#Upload the csv file
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


#Display according to starting letter and select id accordingly
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
    return render_template("table_display.html",data=rows, stime=e_time)

#Display according to starting letter and select id accordingly with cache
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
                t = "With Cache"
                print(t)
                isCache = 'with Cache'

                rows = pickle.loads(r.get(cache+var))
                #r.delete(cache)

            else:
                t = "Without Cache"
                print(t)
                con = sql.connect("database.db")
                cur = con.cursor()
                cur.execute(query1)
                rows1 = cur.fetchall()
                con.close()
                r.set(cache+var, pickle.dumps(rows))
            end_t = time.time() - start_t
            print(end_t)
            return render_template("table_display.html",data=rows, rows=t, stime=end_t)


#Clustering
@app.route('/cluster',methods=['GET','POST'])
def cluster():
    rows = []
    l=[]
    if request.method=="POST":
        value=int(request.form['c'])
        query = "SELECT mag FROM EARTHQUAKE"
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        y = pd.DataFrame(rows)
        X = y.dropna().to_numpy()
        k = KMeans(n_clusters=value, random_state=0).fit(X)

        l.append(k.cluster_centers_)
        print(l[0][0])
        print(rows)

    return render_template('table.html', data=rows)

#Cluster making Plotting
@app.route('/cluster_plot',methods=['GET','POST'])
def cluster_plot():
    query = "SELECT latitude,longitude FROM Earthquake "
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    y = pd.DataFrame(rows)
    k = KMeans(n_clusters=5, random_state=0).fit(y)
    X = y.dropna()
    print(X[0])
    fig = plt.figure()
    centers = k.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
    plt.scatter(X[0], X[1])
    # print(X[:,0])
    plt.show()
    fig.savefig('static/img.png')
    # print(k.cluster_centers_)
    return render_template("clus_o.html", data=rows)

#Select between lat and lon and distance
@app.route('/select_lat', methods=['GET', 'POST'])
def select_lat():
    res = []
    rows = []
    magnitudes=[]
    if request.method == 'POST':
        loop=int(request.form['loop'])
        for i in range(loop):
            cache = "mycache"
            start_t = time.time()
            query = "select * from Earthquake"
            radius = 6373.0
            if r.get(cache):
                t = "With Cache"
                print(t)
                isCache = 'with Cache'

                rows = pickle.loads(r.get(cache))
                # r.delete(cache)

            else:
                t = "Without Cache"
                print(t)
                con = sql.connect("database.db")
                cur = con.cursor()
                cur.execute(query)
                rows = cur.fetchall()
                s_time = time.time()
                for rows1 in rows:
                    lat1 = math.radians(float(rows1[2]))
                    lon1 = math.radians(float(rows1[3]))
                    dist_lat = lat1 - math.radians(float(request.form['lat1']))
                    dist_lon = lon1 - math.radians(float(request.form['lon1']))
                    c = math.sin(dist_lon / 2) * 2
                    formula = math.sin(dist_lat / 2) * 2 + math.cos(math.radians(float(request.form['lat1']))) * math.cos(
                        lat1) * c
                    # print(formula)
                    ans = 2 * (math.atan2(sqrt(abs(formula)), 1 - sqrt(abs(formula))))
                    distance = float(radius * ans)

                    # print(distance)
                    if distance <= (float(request.form['dis'])):
                        # if rows not in res:
                        res.append((rows1[2], rows1[3]))
                con.close()
            r.set(cache, pickle.dumps(res))
            e_time = time.time() - start_t
            print(e_time)
            return render_template("table_display.html",data=rows,rows=t, stime=e_time)

#between two magnitudes
@app.route("/between",methods=['GET','POST'])
def between():
    if request.method=='POST':
        mag1=float(request.form['mag1'])
        mag2=float(request.form['mag2'])
        for i in range(100):
            cache = "mycache"
            start_t = time.time()
            query = "select * from Earthquake where mag between "+str(mag1)+" and "+str(mag2)+""
            if r.get(cache):
                t = "With Cache"
                print(t)
                isCache = 'with Cache'

                rows = pickle.loads(r.get(cache))
                #r.delete(cache)

            else:
                t = "Without Cache"
                print(t)
                con = sql.connect("database.db")
                cur = con.cursor()
                cur.execute(query)
                rows = cur.fetchall()
                con.close()
                r.set(cache, pickle.dumps(rows))
            end_t = time.time() - start_t
            print(end_t)
            return render_template("table_display.html",data=rows, rows=t, stime=end_t)


#Select between two mags and 2 dates
@app.route("/between_dates",methods=['GET','POST'])
def between_dates():
    if request.method=='POST':
        mag1=float(request.form['mag1'])
        mag2=float(request.form['mag2'])
        date1 = (request.form['date1'])
        date2 = (request.form['date2'])
        for i in range(100):
            cache = "mycache"
            start_t = time.time()
            query = 'SELECT * FROM Earthquake where mag BETWEEN ' + str(mag1)+ ' and ' + str(mag2) + ' AND (SUBSTR(time, 1, 10)) >=\'' + date1 + '\' and (SUBSTR(time, 1, 10)) <=   \'' + date2 + '\''
            if r.get(cache):
                t = "With Cache"
                print(t)
                isCache = 'with Cache'

                rows = pickle.loads(r.get(cache))
                #r.delete(cache)

            else:
                t = "Without Cache"
                print(t)
                con = sql.connect("database.db")
                cur = con.cursor()
                cur.execute(query)
                rows = cur.fetchall()
                con.close()
                r.set(cache, pickle.dumps(rows))
            print(rows)
            end_t = time.time() - start_t
            print(end_t)
            return render_template("table_display.html",data=rows, rows=t, stime=end_t)

#Delete Cache
@app.route('/delete',methods=['GET','POST'])
def delete():
    r.flushdb()
    return "Deleted all the Cache!!!"

#select given locationSource
@app.route('/loc',methods=['GET','POST'])
def loc():
    if request.method=='POST':
        location=(request.form['loc'])
        for i in range(100):
            cache = "mycache"
            start_t = time.time()
            query = "select * from earthquake where locationSource ='" + location + "'"
            if r.get(cache):
                t = "With Cache"
                print(t)
                isCache = 'with Cache'

                rows = pickle.loads(r.get(cache))
                #r.delete(cache)

            else:
                t = "Without Cache"
                print(t)
                con = sql.connect("database.db")
                cur = con.cursor()
                cur.execute(query)
                rows = cur.fetchall()
                con.close()
                r.set(cache, pickle.dumps(rows))
            end_t = time.time() - start_t
            print(end_t)
            return render_template("table_display.html",data=rows, rows=t, stime=end_t)


if __name__ == '__main__':
  app.run()
