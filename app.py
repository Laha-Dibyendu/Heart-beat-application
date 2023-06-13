from flask import Flask
from helpers.push_to_db import *
from helpers.heart_beat_checker import *

app = Flask(__name__)# Intitializing the application

from views import *

# Running the app on port 5003
if __name__ == "__main__":
    
    app.run(debug="true", port=5003)