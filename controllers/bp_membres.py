from flask import Blueprint, request, render_template, g, session
from ..authentication import authentication_required
from database.db_general import Database
from ..language.membres import *


membres_bp = Blueprint('members_list', __name__)


@membres_bp.route('/membres')
@authentication_required
def members_list():
    lang = request.cookies.get('lang')
    if 'level' in session:
        if session['level'] is 1:
            members = get_db().get_members_circonscription(session["committee"])
        elif session['level'] is 2:
            members = get_db().get_members_regional(session["committee"])
        elif session['level'] is 3:
            members = get_db().get_members_national(session["committee"])
    if lang == 'english':
        text_content = membres_content_en
    else:
        text_content = membres_content_fr
    return render_template('membres.html', title='Membres', members=members, lang=lang, text=text_content)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database
