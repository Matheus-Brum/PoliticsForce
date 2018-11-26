from flask import Blueprint, render_template, g
from ..authentication import authentication_required
from ..database import Database

modifier_membre_no_bp = Blueprint('modify_member', __name__)


@modifier_membre_no_bp.route('/modifier_membre/<member_no>')
@authentication_required
def modify_member(member_no):
    member = get_db().search_member(member_no)
    return render_template('modifier-membre.html', title='Modifier membre', member=member)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database
