from flask import Blueprint, request, render_template, g, jsonify
from database.queries.Committee_queries import CommitteeQueries
from database.queries.User_queries import UserQueries
import member
from authentication import authentication_admin


api_users_bp = Blueprint('api_users', __name__)


@api_users_bp.route('/api/users')
# @authentication_admin
def users_info():
    users = UserQueries().get_all_users()
    users_regrouped = get_db().occurrence_in_committees_u()
    data = jsonify(users_data=[e.serialize() for e in users], users_total=len(users), occurences=users_regrouped)
    return data


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = CommitteeQueries()
    return g._database
