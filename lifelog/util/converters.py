"""Set of functions for converting URL elements to and from python objects
"""
from werkzeug.routing import BaseConverter

try:
    from pymongo import ObjectId
except:
    from bson.objectid import ObjectId

from lifelog import db, app

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
        username,name = value.split(":")
        user = db.users.find_one({"username":username})
        return db.types.find_one({"name":name, "user" : user['_id']})

    def to_url(self, value):
        username = db.users.find_one(value['user'])['username']
        return str(username + ":" + value['name'])

app.url_map.converters['statname'] = StatNameConverter


class UsernameConverter(BaseConverter):
    """Turn a username into a user object and vica versa"""

    def to_python(self, value):
        return db.users.find_one({"username" : value})

    def to_url(self, value):
        return value['username']

app.url_map.converters['user'] = UsernameConverter
