from flask import Blueprint, request, render_template, g, session
from ..authentication import authentication_required
from ..database.queries.Member_queries import MemberQueries
from ..language.rechercher_membre import *

envois_recherche_bp = Blueprint('recherche_membre_send', __name__)


@envois_recherche_bp.route('/envois_recherche', methods=['POST'])
@authentication_required
def recherche_membre_send():
    lang = request.cookies.get('lang')
    committee = session["committee"]
    level = session["level"]
    if lang == 'english':
        text_content = rechercher_membre_content_en
    else:
        text_content = rechercher_membre_content_fr

    search_by = request.form['search_input']
    search_for = request.form['search_data']
    search_col = recherche_membre(search_by, search_for)

    if search_col is "":
        return render_template('rechercher_membre.html', title="donnees invalides",
                               erreur="error_invalid_selection", text=text_content)
    elif search_for is "":
        return render_template('rechercher_membre.html', title="donnees invalides",
                               erreur="error_invalid_data", text=text_content)
    else:
        result = get_db().search_members(search_col, search_for, committee, level)
        if not result:
            return render_template('rechercher_membre.html', title=search_for, erreur="no_result", lang=lang,
                                   text=text_content)
        else:
            return render_template('rechercher_membre.html', title=search_for, members=result, lang=lang,
                                   text=text_content)


def recherche_membre(search_by, search_for):
    search_col = ""
    if search_by is not "" and search_for is not "":
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
    return search_col


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = MemberQueries()
    return g._database
