from flask import Blueprint, redirect, g
from ..database.queries.Member_queries import MemberQueries
from authentication import authentication_required


membres_no_bp = Blueprint('sup_member', __name__)


@membres_no_bp.route('/membres/<member_no>')
@authentication_required
def sup_member(member_no):
    get_db().supprimer_member(member_no)
    return redirect('/membres')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = MemberQueries()
    return g._database
