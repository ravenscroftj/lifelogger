"""Set of functions for converting URL elements to and from python objects
"""
import re
from werkzeug.routing import BaseConverter

try:
    from pymongo import ObjectId
except:
    from bson.objectid import ObjectId

from lifelog import db, app

def slugify( input ):
    return 

class StatIDConverter(BaseConverter):
    """Turn a statistic ID into a stat object and vica versa
    """

    def to_python(self, value):
        return db.types.find_one(ObjectId(value))

    def to_url(self, value):
        return str(value['_id'])

app.url_map.converters['statid'] = StatIDConverter

class StatNameConverter(BaseConverter):
    """Turn a statistic ID into a stat object and vica versa
    """

    def to_python(self, value):
        username,name = value.replace("_"," ").split(":")

        print re.escape(username)
        user = db.users.find_one({"username": re.compile(username, re.IGNORECASE) })
        
        return db.types.find_one({"name": re.compile(name, re.IGNORECASE) , "user" : user['_id']})

    def to_url(self, value):
        username = db.users.find_one(value['user'])['username']
        return str(username + ":" + value['name']).lower().replace(" ","_")

app.url_map.converters['statname'] = StatNameConverter


class UsernameConverter(BaseConverter):
    """Turn a username into a user object and vica versa"""

    def to_python(self, value):
        return db.users.find_one({"username" : value})

    def to_url(self, value):
        return value['username']

app.url_map.converters['user'] = UsernameConverter
