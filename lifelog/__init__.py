import datetime

from flask import Flask
from pymongo import MongoClient, ASCENDING, DESCENDING

app = Flask(__name__)
app.config.from_pyfile('application.cfg', silent=True)

client = MongoClient("localhost", 27017)
db = client.lifelog

import lifelog.util.converters
import lifelog.web
import lifelog.api

def install_mongo():

   stats = db.stats
   stats.create_index([("date", DESCENDING)])

def main():
    """Main entrypoint for lifelog server"""
    app.run(debug=True, host="0.0.0.0")


if __name__ == "__main__":
    main()
