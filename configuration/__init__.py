from app import app
import urllib
import os

# secret key for user session
app.secret_key = "ITSASECRET"

#setting up mail
app.config['MAIL_SERVER']='smtp.gmail.com' #mail server
app.config['MAIL_PORT'] = 587 #mail port
app.config['MAIL_USERNAME'] = 'in22labs.dibyendu@gmail.com' #email
app.config['MAIL_PASSWORD'] = 'faxdlnkegxiubjyw' #password
app.config['MAIL_USE_TLS'] = True #security type
app.config['MAIL_USE_SSL'] = False #security type

#database connection parameters
connection_params = {
    'user': 'MongoDB',
    'password': "MongoDB",
    'host': "localhost",
    'port': '27017',
    'namespace': '',
}
