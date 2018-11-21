from flask import Blueprint, session, redirect, g
from ..authentication import authentication_required
from ..database import Database


logout_bp = Blueprint('logout', __name__)


@logout_bp.route('/logout')
@authentication_required
def logout():
    if "id" in session:
        id_session = session["id"]
        session.pop('id', None)
        get_db().delete_session(id_session)
    return redirect("/")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database