"""Restful API for the application
"""
import time

from flask import request, jsonify

from lifelog import db, app
from lifelog.model.stats import add_reading

@app.route("/api/submit/<stat:stat>", methods=['POST'])
def submit_statistic(stat):
    """Save a statistic to the server
    
    Expects a post with the relevant fields:

    timestamp - unix timestamp

    stat_name - the name of the statistic to add the data to
    
    """
    values = {x:request.values[x] for x in request.values}

    if 'timestamp' not in values:
        values['timestamp'] = time.time()

    return jsonify({"id":str(add_reading(stat, values))})

