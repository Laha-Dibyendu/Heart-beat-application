import requests
import smtplib
from email.mime.text import MIMEText
import psycopg2
import time
from helpers.ssl_checker import *
from helpers.push_to_db import *
import configparser

# importing details from config.ini
config2 = configparser.ConfigParser()
config2.read('configuration\config_db.ini')  # reading the config file
host = config2.get('postgresql', 'host')  # getting host id
database = config2.get('postgresql','database')
user = config2.get('postgresql','user')
password_db = config2.get('postgresql','password')
port = config2.get('postgresql', 'port') 

payload = {}
headers = {}

# Method to write website grade to db
def grading(urls):
    for ur in urls:
        p= check_grade_ssl(ur[1])
        ans=fetch_ssl_grade_db()
        if ans:
            flag=False
            for elem in ans:
                if  ur[0]  in elem:
                    flag=True
                    break
            if flag:
                update_ssl_grade_db(ur[0],p) 
            else:     
                write_ssl_grade_db(ur[0],p)        
        else:
            write_ssl_grade_db(ur[0],p)

# Method to fetch grade
def fetching_grade():
    ans=fetch_ssl_grade_db()
    total=[]
    if ans :
        for row in ans:
            temp=[]
            b=get_Url_name_db(row[2])
            c=row[1]
            temp.append(b[0])
            temp.append(b[1])
            temp.append(c)
            total.append(temp)
    return total

# Grade checker
def check_grade_ssl(url,payload={}, headers={}):
    url_fin = "https://api.ssllabs.com/api/v3/analyze?host="+(url.split(":")[1][2:]).split("/")[0]
    print(url_fin)
    response = requests.request("GET", url_fin, headers=headers, data=payload).json()
    print(response)
    if "status"not in response.keys() or response["status"]=="Error":
        return "Can't fetch"
    else:
        while "endpoints" not in response.keys() :
            response = requests.request("GET", url_fin, headers=headers, data=payload).json()
        print([l.keys() for l in response["endpoints"]])
        while "grade" not in [l.keys() for l in response["endpoints"]][0]:
            response = requests.request("GET", url_fin, headers=headers, data=payload).json()
        return response["endpoints"][0]["grade"]

# Url aliveness checker method
def check_1(urls, payload={}, headers={}):
    time_stamp = int(time.time())
    for url in urls:
        try:
            response = requests.request(
                "GET", url[1], headers=headers, data=payload)
            # checks if the status code starts with 2 
            if str(response.status_code).startswith('2'):
                # connect to the database
                ans = get_status1_db(url[0])
                if ans !=None:
                    if ans[0] == "Dead":
                        update_status_db("Alive", response.status_code, time.time() ,time.time(),url[0])
                        send_email("Website Live again", "The website {} is live again".format(url[1]))
                else:    
                    write_to_status_db("Alive", response.status_code, time.time() ,time.time(),url[0])
                database_commit(url, response, time_stamp)
                print("Printed in the database successfully")
            else:
                if ans!=None:
                    if ans[0] == "Alive":
                        update_status_db("Dead", response.status_code, time.time() ,time.time(),url[0])
                        send_email("Website is down", "The website {} is down now".format(url[1]))
                else:    
                    write_to_status_db("Down", response.status_code, time.time() ,time.time(),url[0])
                database_commit(url, response, time_stamp)
                print("Printed in the database successfully but task failed")
                send_email("Task Failed", "The status code for the api call of {} has returned ".format(url[1])+str(response.status_code))
        except Exception as e:
            write_to_status_db("Down", 404, time.time() ,time.time(),url[0])
            write_to_server_db(time.time(),url[1],404,"Can't Measure",None)
            send_email("Task Failed", str(e)+"for the website {}".format(url))

# Commiting aliveness to the database
def database_commit(url, response, time_stamp):
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
    # create a cursor object
    cur = conn.cursor()
    # create a table
    cur.execute("CREATE TABLE IF NOT EXISTS servertable (id SERIAL PRIMARY KEY, timestamp INTEGER, url VARCHAR NOT NULL, status_code VARCHAR NOT NULL,ssl_expiry VARCHAR, description VARCHAR)")
    hostname = url[1].split("/")[2]
    try:
        print(get_ssl_expiry_date(hostname))
        expire_date = get_ssl_expiry_date(hostname)
        now = datetime.datetime.now()
        # calculate the difference between the expiration date and the current date
        time_left = expire_date - now
        # check if the time left is less than or equal to 1 day
        if int(time_left.days)<= 10:
            send_email("Expiry Date is Near", "Time left for SSL expiry is {} .The expiry date of the website {} is {}".format(time_left.days,hostname,expire_date))
    except:
        expire_date = None
    # insert some data into the table
    fet= get_ssl1_db(url[0]) or None
    if fet :
        if fet[0]==expire_date:
            pass
        else:
            update_ssl_db(expire_date,url[0])
    else:
        write_to_ssl_db(expire_date,url[0])

    cur.execute("INSERT INTO servertable (timestamp, url, status_code,ssl_expiry, description) VALUES (%s,%s,%s,%s, %s)",
                 (time_stamp, url[1], int(response.status_code), expire_date, response.text))
    conn.commit()
    # close the cursor and connection
    cur.close()
    conn.close()

# Function which sends mail
def send_email(subject, body):#, sender_email, receiver_email, smtp_server, smtp_port, smtp_username, smtp_password):
    message = MIMEText(body)
    message['Subject'] = subject
    # importing details from config.ini
    config = configparser.ConfigParser()
    config.read('configuration\config_mail.ini')
    sender_email= config.get('DEFAULT', 'sender_email')
    receiver_email= config.get('DEFAULT', 'receiver_email')
    smtp_server= config.get('DEFAULT', 'smtp_server')
    smtp_port= config.get('DEFAULT', 'smtp_port')
    smtp_password = config.get('DEFAULT', 'smtp_password')
    message['From'] = sender_email
    message['To'] = receiver_email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
    print("Email sent successfully!")