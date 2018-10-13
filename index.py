from .database import Database
from .member import Member
from flask import g
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re

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
    return render_template('ajouter-membre.html', title='Ajouter')

@app.route('/membres/<member_no>')
def sup_member(member_no):
    get_db().supprimer_member(member_no)
    return redirect('/membres')


@app.route('/envois_ajout', methods=['POST'])
def add_member_send():
    regex = '^\d\.{2}[0-9]'
    f_name = request.form['first_name']
    l_name = request.form['last_name']
    member_no = request.form['member_no']
    phone_no = request.form['phone_no']
    mem_exp_date = request.form['expiring_date']
    reach_moment = request.form['reach_day']
    birth_date = request.form['birth_date']
    email = request.form['email']
    last_donation = request.form['last_donation']
    date_last_donation = request.form['last_donation_date']
    donation_ok = request.form['donated']
    election_year = request.form['elec_year']
    comment = request.form['comment']
    address = request.form['address']

    new_member = Member(f_name, l_name, member_no, phone_no, mem_exp_date, reach_moment, birth_date, email, last_donation,
                        date_last_donation, donation_ok, election_year, comment, address)

    if new_member.f_name is not None and new_member.l_name is not None and new_member.member_no\
            is not None and new_member.phone_no is not None and new_member.address is not None\
            and new_member.email is not None and new_member.last_donation is not None\
            and new_member.last_donation_date is not None\
            and len(new_member.member_no) == 10\
            and len(new_member.phone_no) == 10\
            and new_member.address is not None\
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
def members_list():
    members = get_db().get_all_members()
    return render_template('membres.html', title='Liste', members=members)


@app.route('/rechercher_membre')
def recherche_membre():
    return render_template('rechercher-membre.html', title='Rechercher')


@app.route('/envois_recherche', methods=['POST'])
def recherche_membre_send():
    search_by = request.form['search_input']
    search_for = request.form['search_data']
    if search_by is not None and search_for is not None and search_for != '':
        if search_by == 'first_name':
            search_col = 'F_name'
        elif search_by == 'last_name':
            search_col = 'L_name'
        elif search_by == 'id_no':
            search_col = 'Id'
        elif search_by == 'phone_no':
            search_col = 'Phone_no'
        elif search_by == 'addrese':
            search_col = 'Address'
        else:
            return render_template('rechercher-membre.html', title="donnees invalides", erreur="Erreur: selection invalides")

        result = get_db().search_members(search_col, search_for)
        return render_template('rechercher-membre.html', title=search_for, members=result)

    else:
        return render_template('rechercher-membre.html', title="donnees invalides", erreur="Erreur: donnees recherches invalides")


@app.route('/afficher_membre/<id>')
def affiche_util(id):
    resultat = get_db().search_member(id)
    return render_template('afficher_membre.html', id=resultat)


@app.route('/async_recherche/<info>')
def async_search(info):
    members = get_db().search_member2(info)
    return render_template('test-async.html', members=members)

