from flask import Blueprint, request, render_template
from ..authentication import authentication_required
from..language.rechercher_membre import *


recherche_membre_bp = Blueprint('recherche_membre', __name__)


@recherche_membre_bp.route('/rechercher_membre')
@authentication_required
def recherche_membre():
    lang = request.cookies.get('lang')
    if lang == 'english':
        text_content = rechercher_membre_content_en
    else:
        text_content = rechercher_membre_content_fr
    return render_template('rechercher_membre.html', title='Recherhcer', lang=lang, text=text_content)
