# coding=utf-8
from .database import Database
from .member import Member
from .language.text_content import *
from flask import g
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import make_response
from flask import Response
from flask import session
from functools import wraps
import random
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
    lang = request.cookies.get('lang')
    email = None
    # print(session["id"])
    print("id" in session)
    if "id" in session:
        email = get_db().get_session(session["id"])
        print(session["id"])
        print("id" in session)
    if lang == 'english':
        text_content = accueil_content_en
    else:
        text_content = accueil_content_fr
    return render_template('accueil.html', title='Home', email=email, lang=lang, text=text_content)


@app.route('/confirmation')
def confirmation_page():
    lang = request.cookies.get('lang')
    if lang == 'english':
        text_content = confirmation_content_en
    else:
        text_content = confirmation_content_fr
    return render_template('confirmation.html', text=text_content)


@app.route('/formulaire', methods=["GET", "POST"])
@authentication_required
def formulaire_creation():
    lang = request.cookies.get('lang')
    if lang == 'english':
        text_content = formulaire_content_en
    else:
        text_content = formulaire_content_fr

    if request.method == "GET":
        pwd = passwordGenerator()
        return render_template("formulaire.html", text=text_content, password=pwd)
    elif request.method == "POST":
        username = request.form["email"]
        password = request.form["password"]

        reg1bool = False
        reg2bool = False
        reg3bool = False
        reg4bool = False

        regex2 = "[A-Z]"
        regex3 = "[0-9]"
        regex4 = "['$', '#', '@', '!', '*']"

        longpass = len(password)

        if username == "" or password == "":
            return render_template("formulaire.html", error="mandatory", text=text_content)
        else:
            if longpass < 11 or longpass > 11:
                reg1bool = False
            elif longpass == 11:
                reg1bool = True
                if re.search(regex2, password) is not None:
                    reg2bool = True
                if re.search(regex3, password) is not None:
                    reg3bool = True
                if re.search(regex4, password) is not None:
                    reg4bool = True

        if reg1bool and reg2bool and reg3bool and reg4bool is True:
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(str(password + salt).encode("utf-8")).hexdigest()
            db = get_db()
            print('username', username)
            print('salt', salt)
            print('hashed', hashed_password)
            db.create_user(username, salt, hashed_password)

            return redirect("/confirmation")
        else:
            return render_template("formulaire.html", error="password_requires", text=text_content)


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
    lang = request.cookies.get('lang')
    if lang == 'english':
        text_content = ajouter_membre_content_en
    else:
        text_content = ajouter_membre_content_fr
    return render_template('ajouter_membre.html', title='Ajouter un membre', lang=lang, text=text_content)


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
    lang = request.cookies.get('lang')
    if lang == 'english':
        text_content = ajouter_membre_content_en
    else:
        text_content = ajouter_membre_content_fr
    if new_member.f_name is not None and new_member.l_name is not None and new_member.member_no \
            is not None and new_member.phone_no is not None and new_member.address is not None \
            and new_member.email is not None and new_member.last_donation is not None \
            and new_member.date_last_donation is not None \
            and len(new_member.member_no) == 10 \
            and len(new_member.phone_no) == 10 \
            and re.match(regex, last_donation):

        check_member = get_db().verify_member(new_member)
        if check_member is False:
            get_db().insert_member(new_member)
            return redirect('/')
        else:
            return render_template('ajouter_membre.html', error="add_error", text=text_content)
    else:
        return render_template('ajouter_membre.html', error="add_error", text=text_content)


@app.route('/membres')
@authentication_required
def members_list():
    lang = request.cookies.get('lang')
    members = get_db().get_all_members()
    if lang == 'english':
        text_content = membres_content_en
    else:
        text_content = membres_content_fr
    return render_template('membres.html', title='Membres', members=members, lang=lang, text=text_content)


@app.route('/rechercher_membre')
@authentication_required
def recherche_membre():
    lang = request.cookies.get('lang')
    if lang == 'english':
        text_content = rechercher_membre_content_en
    else:
        text_content = rechercher_membre_content_fr
    return render_template('rechercher_membre.html', title='Recherhcer', lang=lang, text=text_content)


@app.route('/envois_recherche', methods=['POST'])
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
            return render_template('rechercher_membre.html', title=search_by + ":" + search_for,
                                   erreur="no_result", lang=lang, text=text_content)
        else:
            return render_template('rechercher_membre.html', title=search_by + ":" + search_for, members=result,
                                   lang=lang, text=text_content)
    else:
        return render_template('rechercher_membre.html', title="donnees invalides",
                               erreur="error_invalid_data", text=text_content)


@app.route('/afficher_result/<donnees>')
@authentication_required
def afficher_res(donnees):
    lang = request.cookies.get('lang')
    search_by, search_for = donnees.split(":")
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
            if lang == "english":
                text_content = rechercher_membre_content_en
            else:
                text_content = rechercher_membre_content_fr
            return render_template('rechercher_membre.html', title="donnees invalides",
                                   erreur="error_invalid_selection", text=text_content)

        result = get_db().search_members(search_col, search_for)
        if lang == "english":
            text_content = afficher_result_content_en
        else:
            text_content = afficher_result_content_fr
        if not result:
            return render_template('afficher_result.html', title=search_by + ":" + search_for,
                                   erreur="no_result", text=text_content)
        return render_template('afficher_result.html', title=search_by + ":" + search_for, members=result,
                               text=text_content)


@app.route('/afficher_membre/<member_no>')
@authentication_required
def affiche_util(member_no):
    lang = request.cookies.get('lang')
    resultat = get_db().search_member(member_no)
    if lang == "english":
        text_content = afficher_membre_content_en
    else:
        text_content = afficher_membre_content_fr

    return render_template('afficher_membre.html', title='Afficher', id=resultat, lang=lang,
                           text=text_content)


@app.route('/logout')
@authentication_required
def logout():
    if "id" in session:
        id_session = session["id"]
        session.pop('id', None)
        get_db().delete_session(id_session)
    return redirect("/")


@app.route('/language')
def set_to_english():
    response = make_response(redirect('/'))
    language = request.cookies.get('lang')
    print('language', language)
    if 'lang' in request.cookies:
        print('111')
        if language == "francais":
            print('222')
            response.set_cookie("lang", "english")
        else:
            print('333')
            response.set_cookie("lang", "francais")
    else:
        print('444')
        response.set_cookie("lang", "francais")
    return response


def is_authenticated(session):
    return "id" in session


def send_unauthorized():
    lang = request.cookies.get('lang')
    if lang == 'english':
        text_content = page_401_content_en
    else:
        text_content = page_401_content_fr
    return Response(render_template('401.html', text=text_content), 403, {'WWW-Authenticate': 'Basic realm="Login Required"'})


def passwordGenerator():
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    number = '1234567890'
    special = '~!@#$%^&*()[]:<>?'
    password = ""
    for i in range(8):
        password += random.choice(lowercase)
    password += random.choice(uppercase)
    password += random.choice(number)
    password += random.choice(special)
    return ''.join(random.sample(password, len(password)))
