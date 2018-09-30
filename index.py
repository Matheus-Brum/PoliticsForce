from .database import Database
from flask import g
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

app = Flask(__name__)

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


@app.route('/')
def start_page():
    return render_template('accueil.html')


@app.route('/envoyer', methods=['POST'])
def donnees_formulaire():
    prenom = request.form['fname']
    nom = request.form['lname']
    get_db().ajouter(prenom,nom)
    return render_template('accueil.html')

