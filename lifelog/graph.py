"""Graph functions for displaying stats"""

from datetime import datetime
from lifelog import db

from math import ceil

def build_frequency_graph(stat, interval, starttime, endtime):
    """Take a series of timestamps and generate frequency graph
    """
    
    timelength = endtime - starttime
    n = int(ceil(timelength / interval))

    points = []

    for i in range(0,n):
        start = datetime.fromtimestamp( starttime + (i*interval) )
        end   = datetime.fromtimestamp( starttime + ((i+1) * interval) )
        freq = db.records.find({
            "stat" : stat['_id'],
            "date" : {"$gte" : start,
            "$lt"  : end}
            }).count()

        if( freq > 0 ):
            points.append( (start, freq) )
            

    return points



def build_pie_chart( stat, field):
    """Build a pie/distribution chart using a given field"""

    values = db.records.find({"stat": stat['_id']}).distinct(field)

    dist = {}

    for v in values:
        dist[v] = db.records.find({"stat": stat['_id'], field: v}).count()


    return dist
