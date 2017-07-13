import os
import sqlite3
from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'jobber.db')
))


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    filter_ = None
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    c = rv.cursor()
    sql = "SELECT title, label, url FROM job_entries;"
    if request.method == "POST":
        filter_ = request.form["search"]
        t = ('%{}%'.format(filter_.title()), '%{}%'.format(filter_.title()))
        c.execute(("SELECT title, label, url "
                   "FROM job_entries "
                   "WHERE label LIKE ? "
                   "OR title LIKE ?;"), t)
    else:
        c.execute(sql)

    jobs = c.fetchall()

    return render_template("index.html", jobs=jobs, keyword=filter_)
