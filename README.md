# Heart-beat-application
# Read and follow this doc to run the project
* ## "configuration" folder :

    It contains config files for postgres database , mongodb database , mailing credentials, scheduler time configuration

    `__init__.py` - Contains mongodb credentials which is used in the orginal project to store user login details. You have to change this with your mongodb server details.

    `config_db.ini` - Contains the Postgresql credentials which you need to change first.

    `config_mail.ini` - Contains the Mailing credentials which you need to change.

    `config_time.ini` - Contains the scheduler time configurations details which we can change based on how frequently we want to check the aliveness.

# 

* ## "helpers" folder :

    ### From the original project : 

    `database.py` contains mongodb code for storing and retrieving user details.

    `hashpass.py` contains the code for hashing the user login password.

    `mailer.py` contains mailing functionality fo sending mail on successful login.

    ### For Heartbeat project :

    `heart_beat_checker.py` - It contains code to check the aliveness of the URLs and stores it in the postgres database. It also has `send_email` function which is used to send mail in case of website is down.

    `push_to_db.py` - Contains all the code for writing and fetching data from various tables of postgres.

    `ssl_checker.py` - Contains code for checking the SSL expiry date of URLs.

#

## "model" folder :

It contains code for Login and register and password checks.

#

## "views" folder :

The `__init__.py` file contains all the end points of flask which we are using to access various pages of our application.

#

## `app.py`

It contains  the code for initializing the flask application.

#

## To RUN the `app.py` :
* Open the project folder in the terminal. Create virtual environment.
    
    `python -m venv env`

* Activate the virtual environment

    `.\env\scripts\activate`

* Install all the requirements through 

    `pip install -r requirements.txt`

* Run the `app.py` through this command

    `python app.py`

* Go to this URL to see the dashboard 

    `http://127.0.0.1:5003/` give this as the URL

