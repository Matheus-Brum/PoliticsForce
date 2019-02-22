from flask import Blueprint, render_template
from authentication import authentication_admin

entry_point_bp = Blueprint('entry_point', __name__)


@entry_point_bp.route('/api')
# @authentication_admin
def entry_point():
    return render_template('api_entry.html', title='API')
