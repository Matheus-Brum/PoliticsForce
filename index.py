# coding=utf-8
from .database import Database
from .member import Member
from flask import g
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import Response
from flask import session
from functools import wraps
import uuid
import hashlib
import re

app = Flask(__name__)
app.debug = True
app.static_folder = 'static'
app.secret_key = "(*&*&322387he738220)(*(*22347657"


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


def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return send_unauthorized()
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def home():
    email = None
    if "id" in session:
        email = get_db().get_session(session["id"])
        print(session["id"])
        print("id" in session)
    return render_template('accueil.html', title='Accueil', email=email)


@app.route('/confirmation')
def confirmation_page():
    return render_template('confirmation.html')


@app.route('/formulaire', methods=["GET", "POST"])
def formulaire_creation():
    if request.method == "GET":
        return render_template("formulaire.html")
    else:
        username = request.form["email"]
        password = request.form["password"]
        if username == "" or password == "":
            return render_template("formulaire.html",
                                   error="Tous les champs sont obligatoires.")

        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(str(password + salt).encode("utf-8")).hexdigest()
        db = get_db()
        db.create_user(username, salt, hashed_password)

        return redirect("/confirmation")


@app.route('/login', methods=['POST'])
def log_user():
    email = request.form['email']
    password = request.form['password']
    if email is "" or password is "":
        return redirect("/")
    else:
        auth = get_db().get_credentials(email, password)
        if auth is False:
            return redirect("/")
        else:
            session["id"] = get_db().save_session(email)
            session["email"] = email
            return redirect("/")


@app.route('/ajouter_membre')
@authentication_required
def add_member():
    return render_template('ajouter-membre.html', title='Ajouter')


@app.route('/membres/<member_no>')
@authentication_required
def sup_member(member_no):
    get_db().supprimer_member(member_no)
    return redirect('/membres')


@app.route('/envois_ajout', methods=['POST'])
@authentication_required
def add_member_send():
    f_name = request.form['first_name']
    l_name = request.form['last_name']
    member_no = request.form['member_no']
    phone_no = request.form['phone_no']
    country = request.form['country']
    state = request.form['province']
    city = request.form['city']
    postal_code = request.form['code-postal']
    apt = request.form['appartement']
    email = request.form['email']
    last_donation = request.form['last_donation']
    date_last_donation = request.form['last_donation_date']
    donation_ok = request.form['donated']
    election_year = request.form['elec_year']
    mem_exp_date = request.form['expiring_date']
    reach_moment = request.form['reach_day']
    birth_date = request.form['birth_date']
    comment = request.form['comment']

    regex = '^\d+(\.\d*)?|\.\d+'
    address = ""
    if apt != "":
        address += apt + "," + postal_code + "," + city + "," + state + "," + country
    else:
        address += postal_code + "," + city + "," + state + "," + country
    
    new_member = Member(f_name, l_name, member_no, phone_no, mem_exp_date, 
                        reach_moment, birth_date, email, last_donation, 
                        date_last_donation, donation_ok, election_year, 
                        comment, address)
    print('member=', new_member)
    if new_member.f_name is not None and new_member.l_name is not None and new_member.member_no\
            is not None and new_member.phone_no is not None and new_member.address is not None\
            and new_member.email is not None and new_member.last_donation is not None\
            and new_member.date_last_donation is not None\
            and len(new_member.member_no) == 10\
            and len(new_member.phone_no) == 10\
            and re.match(regex, last_donation):

        check_member = get_db().verify_member(new_member)
        if check_member is False:
            get_db().insert_member(new_member)
            return redirect('/')
        else:
            return render_template('ajouter-membre.html', erreur="erreur d'ajout")
    else:
        return render_template('ajouter-membre.html', erreur="erreur d'ajout")


@app.route('/membres')
@authentication_required
def members_list():
    members = get_db().get_all_members()
    return render_template('membres.html', title='Liste', members=members)


@app.route('/rechercher_membre')
@authentication_required
def recherche_membre():
    return render_template('rechercher-membre.html', title='Rechercher')


@app.route('/envois_recherche', methods=['POST'])
@authentication_required
def recherche_membre_send():
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
            return render_template('rechercher-membre.html', title="donnees invalides",
                                   erreur="Erreur: selection invalides")

        result = get_db().search_members(search_col, search_for)
        if not result:
            return render_template('rechercher-membre.html', title=search_for, erreur="Aucun résultat trouver")
        return render_template('rechercher-membre.html', title=search_for, members=result)

    else:
        return render_template('rechercher-membre.html', title="donnees invalides",
                               erreur="Erreur: donnees recherches invalides")


@app.route('/afficher_membre/<member_no>')
@authentication_required
def affiche_util(member_no):
    resultat = get_db().search_member(member_no)
    return render_template('afficher_membre.html', id=resultat)


@app.route('/logout')
@authentication_required
def logout():
    if "id" in session:
        id_session = session["id"]
        session.pop('id', None)
        get_db().delete_session(id_session)
    return redirect("/")


def is_authenticated(session):
    return "id" in session


def send_unauthorized():
    return Response(render_template('401.html'), 403, {'WWW-Authenticate': 'Basic realm="Login Required"'})
