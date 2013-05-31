"""Set of functions for converting URL elements to and from python objects
"""
from werkzeug.routing import BaseConverter

try:
    from pymongo import ObjectId
except:
    from bson.objectid import ObjectId

from lifelog import db, app

class StatConverter(BaseConverter):
    """Turn a statistic ID into a stat object and vica versa
    """

    def to_python(self, value):
        return db.types.find_one(ObjectId(value))

    def to_url(self, value):
        return str(value['_id'])

app.url_map.converters['stat'] = StatConverter
