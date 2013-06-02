"""Graph functions for displaying stats"""

from datetime import datetime
from lifelog import db

from math import ceil

def build_frequency_graph(stat, interval, starttime, endtime):
    """Take a series of timestamps and generate frequency graph
    """
    
    timelength = endtime - starttime
    n = int(ceil(timelength / interval))

    print timelength

    points = []

    for i in range(0,n):
        start = datetime.fromtimestamp( starttime + (i*interval) )
        end   = datetime.fromtimestamp( starttime + ((i+1) * interval) )
        print start
        print end
        freq = db.records.find({
            "stat" : stat['_id'],
            "date" : {"$gte" : start,
            "$lt"  : end}
            }).count()

        if( freq > 0 ):
            points.append( (start, freq) )
            

    return points
