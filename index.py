# coding=utf-8

from .forms.bp_envois_ajout import envois_ajout_bp
from .forms.bp_envois_recherche import envois_recherche_bp
from .forms.bp_formulaire import formulaire_bp
from .forms.bp_login import login_bp
from .forms.bp_envois_modification import envois_modification_bp

from .controllers.bp_language import language_bp
from .controllers.bp_afficher_membre_no import afficher_membre_no_bp
from .controllers.bp_ajouter_membre import ajouter_membre_bp
from .controllers.bp_confirmation import confirmation_bp
from .controllers.bp_logout import logout_bp
from .controllers.bp_rechercher_membre import recherche_membre_bp
from .controllers.bp_membres_no import membres_no_bp
from .controllers.bp_afficher_result_donnees import afficher_result_donnees_bp
from .controllers.bp_membres import membres_bp
from .controllers.bp_home import home_bp
from .controllers.bp_modifier_membre import modifier_membre_no_bp

from .database import Database
import random
from flask import g
from flask import Flask


app = Flask(__name__)
app.debug = True
app.static_folder = 'static'
app.secret_key = "(*&*&322387he738220)(*(*22347657"

app.register_blueprint(envois_recherche_bp)
app.register_blueprint(envois_ajout_bp)
app.register_blueprint(formulaire_bp)
app.register_blueprint(login_bp)

app.register_blueprint(home_bp)
app.register_blueprint(afficher_result_donnees_bp)
app.register_blueprint(membres_no_bp)
app.register_blueprint(recherche_membre_bp)
app.register_blueprint(confirmation_bp)
app.register_blueprint(language_bp)
app.register_blueprint(afficher_membre_no_bp)
app.register_blueprint(ajouter_membre_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(membres_bp)
app.register_blueprint(modifier_membre_no_bp)
app.register_blueprint(envois_modification_bp)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()
