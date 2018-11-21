from flask import Blueprint, request, render_template, g
from ..authentication import authentication_required
from ..database import Database
from ..language.membres import *


membres_bp = Blueprint('members_list', __name__)


@membres_bp.route('/membres')
@authentication_required
def members_list():
    lang = request.cookies.get('lang')
    members = get_db().get_all_members()
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
