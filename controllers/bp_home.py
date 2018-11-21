from flask import Blueprint, render_template,request, session, g
from ..database import Database
from ..language.accueil import *


home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home():
    lang = request.cookies.get('lang')
    email = None
    circonscription = None
    # print(session["id"])
    print("id" in session)
    if "id" in session:
        email = get_db().get_session(session["id"])[0]
        circonscription = get_db().get_session(session["id"])[1]

        print(session["id"])
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
