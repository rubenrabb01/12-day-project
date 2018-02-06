from flask import Flask, render_template, request, redirect
from os.path import abspath, dirname, join
from flask import flash, Flask, Markup, redirect, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import fields
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import webbrowser


app = Flask(__name__)

_cwd = dirname(abspath(__file__))



app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy(app)

        
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')



if __name__ == '__main__':
  app.run(host='0.0.0.0')
