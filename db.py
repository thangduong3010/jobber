import sqlite3
from jobber.route import app


def connect_db():
    """ Connects to the specific database. """
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    queries = open('schema.sql').read().split(';')
    db = connect_db()
    for query in queries:
        db.cursor().execute(query)
    db.commit()
