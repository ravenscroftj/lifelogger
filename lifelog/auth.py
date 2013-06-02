"""
Authentication module for lifelog

"""
from crypt import crypt
from flask import request, session, redirect, url_for, abort
from lifelog import db, app
from functools import wraps

class AuthenticationException(Exception):
    pass

#----------------------------------------------------------------------
def current_user():
    db.users.ensure_index("username")
    try:
        return db.users.find_one({"username" : session['username']})
    except KeyError:
        return None
#----------------------------------------------------------------------

def login(username, password):
    """Log in using username password pair"""

    user = db.users.find_one({"username" : username})
    
    if user == None:
        raise AuthenticationException("No user with name '%s' found" % username)
    pw = user['password']

    user = db.users.find_one({"username":username, "password":crypt(password, pw)})

    if user == None:
        raise AuthenticationException("Username/Password pair invalid")
    else:
        session['logged_in'] = True
        session['username'] = user['username']


#----------------------------------------------------------------------

def logout():
    session.clear()

#----------------------------------------------------------------------

def register(username, password, email):
    """Register a user account"""

    #see if the username has been taken
    if db.users.find_one({"username":username}) != None:
        raise  AuthenticationException("Username '%s' has already been taken" % username)
    #see if the email is taken
    if db.users.find_one({"email":email}) != None:
        raise AuthenticationException("Email %s is already being used" % email)

    #create the user
    id = db.users.insert({"username":username,"password": crypt(password,password[0:2]), "email":email})

    login(username, password)

    return id

#----------------------------------------------------------------------

def require_auth(f, redir=True):
    """Decorator that requires the user to be authenticated or returns 403
    
    Use redir to specify whether the user should be redirected to the login form or 
    
    """
    @wraps(f)
    def wrapped(*args, **kwargs):

        print "MOO"
        
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            if redir:
                return redirect(url_for('login'))
            else:
                return abort(401)

    return wrapped
