from flask import Blueprint, render_template, g
from ..authentication import authentication_required
from ..database.db_general import Database

afficher_result_donnees_bp = Blueprint('afficher_res', __name__)


@afficher_result_donnees_bp.route('/afficher-result/<donnees>')
@authentication_required
def afficher_res(donnees):
    search_by, search_for = donnees.split(":")
    if search_by is not None and search_for is not None and search_for != '':
        if search_by == 'first_name':
            search_col = 'F_name'
        elif search_by == 'last_name':
            search_col = 'L_name'
        elif search_by == 'member_no':
            search_col = 'Member_no'
        elif search_by == 'phone_no':
            search_col = 'Phone_no'
        elif search_by == 'addrese':
            search_col = 'Address'
        else:
            return render_template('rechercher-membre.html', title="donnees invalides",
                                   erreur="Erreur: selection invalides! Recommencer - ")

    result = get_db().search_members(search_col, search_for)
    if not result:
        return render_template('afficher-result.html', title=search_for, erreur="Aucun résultat trouver")
    return render_template('afficher-result.html', title=search_by + ":" + search_for, members=result)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database
