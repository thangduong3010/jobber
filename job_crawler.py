#!/usr/bin/env python3

__doc__ = '''
Description:
    URL = "https://api.github.com/repos/awesome-jobs/vietnam/issues"
    Go to URL and fetch information about job openings
'''


import sqlite3
import requests


URL = "https://api.github.com/repos/awesome-jobs/vietnam/issues"


def job_info(url):
    """ Fetch issue data from Github API via `url`

    :param url: github API's url
    :rtype generator:
    """
    for job in requests.get(url).json():
        yield job


def crawler():
    """ Write fetched data to database """
    job_entries = []
    for job in job_info(URL):
        labels = ""
        if job["labels"]:
            for label in job["labels"]:
                labels += label["name"]
                if job["labels"].index(label) != len(job["labels"]) - 1:
                        labels += ","
        job_entries.append((job["number"], job["id"],
                            job["title"], job["html_url"], labels))

    conn = sqlite3.connect('jobber/jobber.db')
    c = conn.cursor()
    c.executemany(('INSERT OR IGNORE INTO job_entries '
                  'VALUES (?,?,?,?,?)'), job_entries)
    conn.commit()
    conn.close()
