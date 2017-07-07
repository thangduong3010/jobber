Job Opening Searching Application
						
						/ Jobber / (An acquaintance of Uber)

How to use it
1. install the app from the root of the project directory

`pip install --editable .`


2. export environment variable

`export FLASK_APP=jobber`

`export FLASK_DEBUG=true`


3. fetch data

`python job_crawler.py`


3. initialize the database with this command

`flask initdb`


4. batch insert into database

`flask batch`


5. now you can run the app:

`flask run`


access the app via
http://localhost:5000/


6. Searching button is working!


7. test

No tests yet!


						Powered by Flask
