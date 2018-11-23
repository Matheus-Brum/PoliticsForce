from flask import request, redirect, session, Blueprint, g
from ..database import Database

login_bp = Blueprint('log_user', __name__)


@login_bp.route('/login', methods=['POST'])
def log_user():
    email = request.form['email']
    password = request.form['password']
    committee = get_db().get_user(email)[15]
    level = get_db().get_user(email)[19]
    print('committee=', committee)
    print('level', level)
    if email is "" or password is "":
        return redirect("/")
    else:
        auth = get_db().get_credentials(email, password)
        if auth is False:
            return redirect("/")
        else:

            session["id"] = get_db().save_session(email, committee)
            session["email"] = email
            session["committee"] = committee
            session["level"] = level
            return redirect("/")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database
