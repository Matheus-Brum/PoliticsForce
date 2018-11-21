from flask import Blueprint, render_template, request
from ..language.confirmation import *

confirmation_bp = Blueprint('confirmation_page', __name__)


@confirmation_bp.route('/confirmation')
def confirmation_page():
    lang = request.cookies.get('lang')
    if lang == 'english':
        text_content = confirmation_content_en
    else:
        text_content = confirmation_content_fr
    return render_template('confirmation.html', text=text_content)