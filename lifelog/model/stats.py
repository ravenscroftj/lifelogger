"""Model and tools for managing stats"""

from datetime import datetime

from lifelog import db


def add_reading( stat_dict ):

    ts = datetime.fromtimestamp( stat_dict['timestamp'] )
    
    stats = db.records

    return stats.insert({
        "stat" : stat_dict['stat'],
        "date" : ts,
        })


def create_stat( name, description, icon=""):
    """Create a new statistic"""

    types = db.types

    types.insert({"name":name, "description":description, "icon": icon})

