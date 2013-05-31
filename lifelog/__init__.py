import datetime

from flask import Flask
from pymongo import MongoClient, ASCENDING, DESCENDING

app = Flask(__name__)

client = MongoClient("localhost", 27017)
db = client.lifelog

import lifelog.util.converters
import lifelog.web

def install_mongo():

   stats = db.stats
   stats.create_index([("date", DESCENDING)])

def main():
    """Main entrypoint for lifelog server"""
    app.run(debug=True)


if __name__ == "__main__":
    main()
