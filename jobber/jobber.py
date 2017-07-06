import os
import sqlite3
from flask import Flask
from flask import request
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import abort
from flask import render_template
from flask import flash


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'jobber.db'),
	SECRET_KEY='development'
))


def connect_db():
	""" Connects to the specific database. """
	rv = sqlite3.connect(app.config["DATABASE"])
	rv.row_factory = sqlite3.Row
	return rv


def get_db():
	""" Opens a new db connection if there is none yet
	Succcesive calls will return the already established connection
	"""
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
	""" Closes the database at the end of the request. """
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()


def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()


@app.cli.command('initdb')
def initdb_command():
	""" Command to initialize the database. """
	init_db()
	print("Initialized the database.")


@app.route("/")
def index():
	db = get_db()
	cur = db.execute('')
	job_entries = cur.fetchall()
	return render_template("index.html", )