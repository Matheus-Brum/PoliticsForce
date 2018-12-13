from flask import Blueprint, render_template, g, request
from authentication import authentication_required
from database.queries.Member_queries import MemberQueries
from language.modifier_membre import *

modifier_membre_no_bp = Blueprint('modify_member', __name__)


@modifier_membre_no_bp.route('/modifier_membre/<member_no>')
@authentication_required
def modify_member(member_no):
    lang = request.cookies.get('lang')
    if lang == 'english':
        text_content = modifier_membre_content_en
    else:
        text_content = modifier_membre_content_fr
    member = get_db().search_member(member_no)
    return render_template('modifier-membre.html', title='Modifier membre', member=member, text=text_content)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = MemberQueries()
    return g._database
