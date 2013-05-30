import os

from flask import render_template, request, send_from_directory
from werkzeug import secure_filename

from lifelog import db, app
from lifelog.model.stats import create_stat

ICONS_DIR = "/home/james/projects/lifelogserver/lifelog/uploads"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register')
def register():
    
    if request.method == 'POST':
        do_register()
    else:
        return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    """Allow a user to see their dashboard"""
    
    records =   db.stats
    stats =     db.types

    return render_template("dashboard.html", records=records, stats=stats)

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

@app.route("/stats/<id>/record")
def record_stat(id):
    """Add a new recording for the given statistic"""

    if request.method == "POST":
        add_reading(


@app.route("/icons/<filename>")
def send_uploaded_icon(filename):
    return send_from_directory(ICONS_DIR, filename)
