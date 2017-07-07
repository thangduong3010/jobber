#!/usr/bin/env python3

__doc__ = '''
Description:
    URL = "https://api.github.com/repos/awesome-jobs/vietnam/issues"
    Go to URL and fetch information about job openings
'''


import requests


URL = "https://api.github.com/repos/awesome-jobs/vietnam/issues"


def fetch_job_info(url):
    """ Fetch issue data from Github API via `url`

    :param url: github API's url
    :rtype list:
    """
    return requests.get(url).json()


def main():
    """ Write fetched data to SQL file """
    jobs = fetch_job_info(URL)

    filename = 'jobber/insert.sql'

    with open(filename, 'w') as f:
        for job in jobs:
            labels = ""
            if job["labels"]:
                for label in job["labels"]:
                    labels += label["name"]
                    if job["labels"].index(label) != len(job["labels"]) - 1:
                        labels += ","

            sql = """INSERT INTO job_entries
                    VALUES ({0},{1},"{2}","{3}","{4}");\n""".format(
                    job["number"], job["id"],
                    job["title"], job["html_url"], labels)
            f.write(sql)


if __name__ == "__main__":
    main()
