from flask import Blueprint, request, render_template, g
from ..authentication import authentication_required
from database.db_general import Database
from ..language.rechercher_membre import *

envois_recherche_bp = Blueprint('recherche_membre_send', __name__)


@envois_recherche_bp.route('/envois_recherche', methods=['POST'])
@authentication_required
def recherche_membre_send():
    lang = request.cookies.get('lang')
    if lang == 'english':
        text_content = rechercher_membre_content_en
    else:
        text_content = rechercher_membre_content_fr
    search_by = request.form['search_input']
    search_for = request.form['search_data']
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
            return render_template('rechercher_membre.html', title="donnees invalides",
                                   erreur="error_invalid_selection", text=text_content)

        result = get_db().search_members(search_col, search_for)
        if not result:
            return render_template('rechercher_membre.html', title=search_for, erreur="no_result", lang=lang, text=text_content)
        else:

            return render_template('rechercher_membre.html', title=search_for, members=result, lang=lang, text=text_content)
    else:
        return render_template('rechercher_membre.html', title="donnees invalides",
                               erreur="error_invalid_data", text=text_content)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database
