from flask import Blueprint, request, render_template
from authentication import authentication_required
from language.ajouter_membre import *


ajouter_membre_bp = Blueprint('add_member', __name__)


@ajouter_membre_bp.route('/ajouter_membre')
@authentication_required
def add_member():
    lang = request.cookies.get('lang')
    if lang == 'english':
        text_content = ajouter_membre_content_en
    else:
        text_content = ajouter_membre_content_fr
    return render_template('ajouter_membre.html', title='Ajouter un membre', lang=lang, text=text_content)