from .database import Database
from flask import g
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

app = Flask(__name__)
app.debug = True


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
def home():
    return render_template('accueil.html', title='Accueil')


@app.route('/ajouter_membre')
def add_member():
    return render_template('ajouter-membres.html', title='Ajouter')


@app.route('/envois_ajout', methods=['POST'])
def add_member_send():
    prenom = request.form['first_name']
    nom = request.form['last_name']
    if prenom and nom is not "" and prenom and nom is not None:
        get_db().insert_member(prenom, nom)
        return redirect(url_for('/'))
    else:
        return 'NOT OK!'

