import os

from time import strftime, strptime, mktime

from flask import render_template, request, send_from_directory, redirect, url_for
from werkzeug import secure_filename

from lifelog import db, app, auth
from lifelog.model.stats import create_stat, add_reading


ICONS_DIR = app.config['UPLOAD_DIR']
TIME_FORMAT = "%m/%d/%Y %H:%M:%S"

@app.route('/')
def index():
    return render_template("index.html")

#----------------------------------------------------------------------

@app.route('/register', methods=['POST','GET'])
def register():
    
    v = request.values
    error = None
    success = False

    if request.method == 'POST':

        error = ""

        #make sure the password stuff validates
        if v['password'] != v['cpassword']:
            error += "Your passwords must match."

        if len(v['password']) < 5:
            error += "Your password must be at least 5 characters long."

        if len(v['email']) < 1:
            error += "You must provide a valid email address."

        if error == "":
            
            error = None

            try:
                print v
                auth.register(v['username'], v['password'], v['email'])
                success = True
            except auth.AuthenticationException as e:
                error = str(e)

    return render_template("register.html", error=error, success=success)

    
#----------------------------------------------------------------------

@app.route("/login", methods=['GET','POST'])
def login():

    error = None

    if request.method == "POST":

        try:
            auth.login(request.values['username'], request.values['password'])
            return redirect(request.values['referrer'] or url_for('.dashboard'))
        except auth.AuthenticationException as e:
            error = str(e)
    
    return render_template("login.html", error=error, referrer=request.referrer)

#----------------------------------------------------------------------

@app.route("/dashboard")
@auth.require_auth
def dashboard():
    """Allow a user to see their dashboard"""

    total_records =   db.records.find({"user": auth.current_user()['_id']}).count()
    stats = []
    for stat in db.types.find({"user": auth.current_user()['_id']}):
        stat['count'] = db.records.find({"stat" : stat['_id']}).count()
        stats.append(stat)

    return render_template("dashboard.html", records=total_records, stats=stats)

#----------------------------------------------------------------------
@app.route("/logout")
@auth.require_auth
def logout():
    """Log out of the LifeLog system"""
    auth.logout()

    return redirect(request.referrer or url_for('.dashboard'))

#----------------------------------------------------------------------

@app.route("/stats/add", methods=['GET', 'POST'])
@auth.require_auth
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

@app.route("/stats/<statid:stat>/record", methods=['GET','POST'])
@auth.require_auth
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
@app.route("/stats/<statname:stat>/view")
def view_stat(stat):
    """Show statistics in a chart"""

    from lifelog.graph import build_frequency_graph, build_pie_chart
    import time
    import datetime
    
    records = db.records.find({"stat" : stat['_id']})


    if 'endtime' in request.values:
        end = datetime.datetime.strptime(request.values['endtime'], 
                TIME_FORMAT)
    else:
        end    = datetime.datetime.now()

    if 'starttime' in request.values:
        start = datetime.datetime.strptime(request.values['starttime'], 
                TIME_FORMAT)
    else:
        start  = end - datetime.timedelta(days=2)

    graph = "timefreq"

    if 'gfield' in request.values:
        graph = "pie"
        points = build_pie_chart(stat, request.values['gfield'])
    else:
        
        if 'scale' in request.values:
            interval = int(request.values['scale'])
        else:
            interval = 3600

        points = build_frequency_graph(stat, interval, int(start.strftime("%s")), int(end.strftime("%s")))


    return render_template("display_stat.html", 
            stat=stat,
            records=records, 
            graph=graph, 
            plots=points, 
            starttime=start, 
            endtime=end)

#----------------------------------------------------------------------

@app.route("/uploads/<filename>")
def send_uploaded_file(filename):
    return send_from_directory(ICONS_DIR, filename)
