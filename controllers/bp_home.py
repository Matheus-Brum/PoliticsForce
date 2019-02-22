from flask import Blueprint, render_template, request, session, g
from database.db_general import Database
from language.accueil import *


home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home():
    lang = request.cookies.get('lang')
    email = None
    committee = None
    level = None
    # print(session["id"])
    # print("id" in session)
    if "id" in session:
        # email = get_db().get_session(session["id"])[0]
        # committee = get_db().get_session(session["id"])[1]
        email = session["email"]
        committee = session["committee"]
        # print(session["email"])
        # print(session["committee"])
        print("id" in session)
    if lang == 'english':
        text_content = accueil_content_en
    else:
        text_content = accueil_content_fr
    return render_template('accueil.html', title='Home', email=email, lang=lang, text=text_content)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database
