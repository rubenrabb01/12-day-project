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

SECRET_KEY = 'flask-session-insecure-secret-key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, 'flask-tracking.db')
SQLALCHEMY_ECHO = True
WTF_CSRF_SECRET_KEY = 'this-should-be-more-random'


app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy(app)

        
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/user')
def index_lulu():
  return render_template('userinfo.html')

@app.route('/test')
def my_page():
    webbrowser.open_new_tab('href="https://github.com/rubenrabb01/12-day-project')




if __name__ == '__main__':
  app.run(host='0.0.0.0')
