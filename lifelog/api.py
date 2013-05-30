"""Restful API for the application
"""

from flask import request, jsonify

from lifelog import db, app
from lifelog.model.stats import add_reading

@app.route("/api/submit", methods=['POST'])
def submit_statistic():
    """Save a statistic to the server
    
    Expects a post with the relevant fields:

    timestamp - unix timestamp

    stat_name - the name of the statistic to add the data to
    
    """
    
    return jsonify({"id":add_reading(request.values)}

