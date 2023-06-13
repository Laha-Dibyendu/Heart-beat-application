from flask import render_template, request, redirect, url_for, session, jsonify
from app import app
from apscheduler.schedulers.background import BackgroundScheduler
import configparser
from model import *
from helpers.push_to_db import *
from helpers.heart_beat_checker import *
import datetime
import threading

#importing details from config_time.ini
config23 = configparser.ConfigParser()
config23.read('configuration\config_time.ini')  # reading the config file
hour = config23.getint('DEFAULT', 'hour')  
minute = config23.getint('DEFAULT','minute')
seconds1 = config23.getint('DEFAULT','seconds')

# Function for the scheduled job, which checks the websites in the given intervals.
def schedule_job():
    urls = []
    url_rows = get_db()
    for row in url_rows:
        if bool(row[3]) == True:
            urls.append((row[0],row[2]))
    check_1(urls)
    print("Just Checked")

# Before the first request wwe will start the scheduler
@app.before_first_request
def activate_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_job,'interval',seconds=hour*60+minute*60+seconds1)
    scheduler.start()
    print("Scheduler started.")

# Index page
@app.route('/', methods=["GET"])
def home():
    if "username" in session:
        ssl= get_ssl_db()
        act= get_status_db()
        active,dead,expiring, ssl_active=0,0,0,0
        for row in act:
            if row[0]=="Alive":
                active+=1
            else:
                dead+=1
        for row_ssl in ssl:
            now = datetime.datetime.now()
            # calculate the difference between the expiration date and the current date
            time_left = datetime.datetime.strptime(row_ssl[0], "%Y-%m-%d %H:%M:%S") - now
            if time_left.days<=10:
                expiring+=1
            else:
                ssl_active+=1
        return render_template('index.html',active=active,dead=dead,expiring=expiring, ssl_active=ssl_active)
    else:
        return render_template('login.html')

# url adding method
@app.route('/submit', methods=['POST'])
def submit():
    # Get the form data
    name = request.form["name"]
    url = request.form["url"]
    is_active = request.form["is_active"]
    site_type = request.form["site_type"]
    # Insert the data into the database
    ans=write(name, url, is_active,site_type)
    return redirect(url_for('home'))

# Updating url data
@app.route('/updates', methods=['POST'])
def submit2():
    # Get the form data
    id = request.form["id"]
    name = request.form["name"]
    url = request.form["url"]
    is_active = request.form["is_active"]
    site_type = request.form["site_type"]
    # Insert the data into the database
    updates(id, name, url, is_active,site_type)
    return redirect(url_for('home'))

# Deleting url
@app.route('/deleted', methods=['GET', 'DELETE'])
def dell():
    id = request.form["id"]
    db_info = del_db(id)
    return {"msg": db_info}

# method to get data for making visualizations
@app.route('/app/line', methods=["GET"])
def charts22():
    labels= sorted([datetime.datetime.fromtimestamp(label[0]) for label in getalltime_serverdb()])
    data = sorted(getcharttime_serverdb())
    dataset=[]
    checker_list=[]
    for d in data :
        name=d[1]
        if name not in checker_list:
            checker_list.append(name)
            min_data=[]
            for li in data:
                count=1
                if name == li[1] and count<len(labels):
                    if d[2]=="200":
                        min_data.append(1)
                    else:
                        min_data.append(0)
                    count+=1
            dataset.append({"label":name, "data":min_data})
    final_data= {"labels":labels, "datasets":dataset}
    return jsonify(final_data)

# SSL grade checking method
@app.route('/ssl_grade', methods=["GET"])
def ssl_grade():
    urls = []
    url_rows = get_db()
    for row in url_rows:
        if bool(row[3]) == True:
            urls.append((row[0],row[2]))
    background_thread = threading.Thread(target=grading(urls))
    background_thread.start()
    grades_data=fetching_grade()
    return render_template('ssl_grade.html', data=grades_data)

#Tables Page
@app.route('/url_table', methods=["GET"])
def tables():
    rows = get_db()
    return render_template("tables.html", rows=rows)

# Log report table
@app.route('/report_table', methods=["GET"])
def tables2():
    rows = get_serverdb()
    return render_template("report-tables.html", rows=rows)

# url aliveness checker
@app.route('/check', methods=['GET'])
def check_live():
    urls = []
    url_rows = get_db()
    for row in url_rows:
        if bool(row[3]) == True:
            urls.append((row[0],row[2]))
    check_1(urls)
    return redirect(url_for('tables2'))

# Register new user
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        registerUser()
        return redirect(url_for("login"))

#Check if email already exists in the registratiion page
@app.route('/checkusername', methods=["POST"])
def check():
    return checkusername()

# Everything Login (Routes to renderpage, check if username exist and also verifypassword through Jquery AJAX request)
@app.route('/login', methods=["GET"])
def login():
    if request.method == "GET":
        if "username" not in session:
            return render_template("login.html")
        else:
            return redirect(url_for("home"))

@app.route('/checkloginusername', methods=["POST"])
def checkUserlogin():
    return checkloginusername()

@app.route('/checkloginpassword', methods=["POST"])
def checkUserpassword():
    return checkloginpassword()

#The admin logout
@app.route('/logout', methods=["GET"])  # URL for logout
def logout():  # logout function
    session.pop('username', None)  # remove user session
    return redirect(url_for("home"))  # redirect to home page with message

#Forgot Password
@app.route('/forgot-password', methods=["GET"])
def forgotpassword():
    return render_template('forgot-password.html')

#404 Page
@app.route('/404', methods=["GET"])
def errorpage():
    return render_template("404.html")

#Blank Page
@app.route('/blank', methods=["GET"])
def blank():
    return render_template('blank.html')

#Buttons Page
@app.route('/buttons', methods=["GET"])
def buttons():
    return render_template("buttons.html")

#Cards Page
@app.route('/cards', methods=["GET"])
def cards():
    return render_template('cards.html')

#Charts Page
@app.route('/charts', methods=["GET"])
def charts():
    return render_template("charts.html")

#Utilities-animation
@app.route('/utilities-animation', methods=["GET"])
def utilitiesanimation():
    return render_template("utilities-animation.html")

#Utilities-border
@app.route('/utilities-border', methods=["GET"])
def utilitiesborder():
    return render_template("utilities-border.html")

#Utilities-color
@app.route('/utilities-color', methods=["GET"])
def utilitiescolor():
    return render_template("utilities-color.html")

#utilities-other
@app.route('/utilities-other', methods=["GET"])
def utilitiesother():
    return render_template("utilities-other.html")
