import os

from time import strftime, strptime, mktime

from flask import render_template, request, send_from_directory
from werkzeug import secure_filename

from lifelog import db, app
from lifelog.model.stats import create_stat, add_reading

ICONS_DIR = app.config['UPLOAD_DIR']
TIME_FORMAT = "%m/%d/%Y %H:%M:%S"

@app.route('/')
def index():
    return render_template("index.html")

#----------------------------------------------------------------------

@app.route('/register')
def register():
    
    if request.method == 'POST':
        do_register()
    else:
        return render_template("register.html")

#----------------------------------------------------------------------

@app.route("/dashboard")
def dashboard():
    """Allow a user to see their dashboard"""
    
    records =   db.records
    stats =     db.types

    return render_template("dashboard.html", records=records, stats=stats)

#----------------------------------------------------------------------

@app.route("/stats/add", methods=['GET', 'POST'])
def add_stat():
    """Create a new statistic type"""

    success = False

    if request.method == 'POST':

        icon = ""

        print request.files

        if len(request.files) > 0:
            image = request.files['icon']
            filename = secure_filename(image.filename)
            image.save(os.path.join(ICONS_DIR, filename))

            icon = filename


        id = create_stat( request.values['name'], request.values['description'], icon)

        success = True
    
    
    return render_template("create_stat.html", success=success)

#----------------------------------------------------------------------

@app.route("/stats/<stat:stat>/record", methods=['GET','POST'])
def record_stat(stat):
    """Add a new recording for the given statistic"""

    success = False

    if request.method == "POST":
        values = {x:request.values[x] for x in request.values}
        values['timestamp'] = mktime(strptime(values['timestamp'], 
            TIME_FORMAT))
        success = ( add_reading(stat, values) != None )
    
    return render_template("add_reading.html", stat=stat, 
            ctime=strftime(TIME_FORMAT),
            success = success)

#---------------------------------------------------------------------
@app.route("/stats/<stat:stat>/view")
def view_stat(stat):
    """Show statistics in a chart"""
    
    records = db.records.find({"stat" : stat['_id']})

    return render_template("display_stat.html", stat=stat,records=records)

#----------------------------------------------------------------------

@app.route("/icons/<filename>")
def send_uploaded_icon(filename):
    return send_from_directory(ICONS_DIR, filename)
