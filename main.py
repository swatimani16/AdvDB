# from flask import Flask
from flask import *
app = Flask(__name__)

@app.route('/')
def hello():
    return "hello flask"

if __name__ == '__main__':
  app.run()
