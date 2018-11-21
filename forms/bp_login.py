from flask import request, redirect, session, Blueprint, g
from ..database import Database

login_bp = Blueprint('log_user', __name__)


@login_bp.route('/login', methods=['POST'])
def log_user():
    email = request.form['email']
    password = request.form['password']
    if email is "" or password is "":
        return redirect("/")
    else:
        auth = get_db().get_credentials(email, password)
        if auth is False:
            return redirect("/")
        else:

            session["id"] = get_db().save_session(email)
            session["email"] = email
            session["circonscription"] = 'Rive-Nord'
            return redirect("/")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database
