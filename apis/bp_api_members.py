from flask import Blueprint, request, render_template, g, jsonify
from database.queries.Committee_queries import CommitteeQueries
import member
from authentication import authentication_admin


api_members_bp = Blueprint('api_members', __name__)


@api_members_bp.route('/api/members')
# @authentication_admin
def members_info():
    members = get_db().get_all_members()
    members_regrouped = get_db().occurrence_in_committees_m()
    data = jsonify(members_data=[e.serialize() for e in members], members_total=len(members), occurences=members_regrouped)
    return data


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = CommitteeQueries()
    return g._database
