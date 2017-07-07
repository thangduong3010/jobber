import os
import sqlite3
from flask import Flask
from flask import request
from flask import g
from flask import render_template
# from flask import session
# from flask import redirect
# from flask import url_for
# from flask import abort
# from flask import flash


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'jobber.db')
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


def retrieve_data(sql):
    """ Retrieve data from database
    using sql
    """
    db = get_db()
    c = db.cursor()
    c.execute(sql)
    return c.fetchall()


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


def batch_db():
    db = get_db()
    with app.open_resource('insert.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('batch')
def batchdb_command():
    """ Batch insert into database. """
    batch_db()
    print("Batch completed.")


@app.route("/", methods=["GET", "POST"])
def index():
    filter_ = None
    sql = "SELECT title, label, url FROM job_entries;"
    if request.method == "POST":
        filter_ = request.form["search"]
        sql = ("SELECT title, label, url "
               "FROM job_entries "
               "WHERE label LIKE '%{0}%' "
               "OR title LIKE '%{1}%';").format(
               filter_.title(), filter_.title())
    jobs = retrieve_data(sql)

    return render_template("index.html", jobs=jobs, keyword=filter_)
