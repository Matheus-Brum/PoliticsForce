from flask import request, render_template, redirect, session, Blueprint, g
from database.queries.User_queries import UserQueries
from database.queries.Session_queries import SessionQueries
from language.accueil import *

login_bp = Blueprint('log_user', __name__)


@login_bp.route('/login', methods=['POST'])
def log_user():
    email = request.form['email']
    password = request.form['password']
    lang = request.cookies.get('lang')
    if lang == 'english':
        text_content = accueil_content_en
    else:
        text_content = accueil_content_fr

    if email is "" or password is "":
        return render_template("/accueil.html", error="mandatory", text=text_content)
    elif email is not "" and password is not "":
        # print("11111")
        if email == 'admin':
            # print('22222')
            auth = get_db().get_admin_credentials(password)
        else:
            auth = get_db().get_credentials(email, password)
        if auth is False:
            return render_template("/accueil.html", error="email_pass", text=text_content)
        else:
            if email == 'admin':
                level = 4
                committee = 'admin'
            else:
                committee = get_db().get_user(email)[15]
                level = get_db().get_user(email)[19]

            session["id"] = SessionQueries().save_session(email, committee, level)
            session["email"] = email
            session["committee"] = committee
            session["level"] = level
            return redirect("/")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = UserQueries()
    return g._database
