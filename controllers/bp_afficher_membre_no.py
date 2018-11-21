from flask import Blueprint,request, render_template, g
from ..authentication import authentication_required
from ..database import Database
from ..language.afficher_membre import *

afficher_membre_no_bp = Blueprint('affiche_util', __name__)


@afficher_membre_no_bp.route('/afficher_membre/<member_no>')
@authentication_required
def affiche_util(member_no):
    lang = request.cookies.get('lang')
    resultat = get_db().search_member(member_no)
    if lang == "english":
        text_content = afficher_membre_content_en
    else:
        text_content = afficher_membre_content_fr

    return render_template('afficher_membre.html', title='Afficher', id=resultat, lang=lang,
                           text=text_content)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database
