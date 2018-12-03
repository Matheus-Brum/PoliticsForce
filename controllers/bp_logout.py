from flask import Blueprint, session, redirect, g
from ..authentication import authentication_required
from database.db_general import Database


logout_bp = Blueprint('logout', __name__)


@logout_bp.route('/logout')
@authentication_required
def logout():
    if "id" in session:
        id_session = session["id"]
        get_db().delete_session(id_session)
        session.pop('id', None)
        session.pop('email', None)
        session.pop('committee', None)
        session.clear()
    return redirect("/")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database
