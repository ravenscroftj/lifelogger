"""Model and tools for managing stats"""

from datetime import datetime

from lifelog import db


def add_reading( stat, dict ):

    ts = datetime.fromtimestamp( float(dict['timestamp']) )
    
    stats = db.records

    dict['timestamp'] = None
    dict['date'] = ts
    dict['stat'] = stat['_id']

    return stats.insert(dict)


def create_stat( name, description, icon=""):
    """Create a new statistic"""

    types = db.types

    types.insert({"name":name, "description":description, "icon": icon})

