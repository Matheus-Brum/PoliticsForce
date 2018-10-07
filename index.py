from .database import Database
from .member import Member
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
    return render_template('ajouter-membre.html', title='Ajouter')

@app.route('/membres/<member_no>')
def sup_member(member_no):
    get_db().supprimer_member(member_no)
    return redirect('/membres')


@app.route('/envois_ajout', methods=['POST'])
def add_member_send():
    f_name = request.form['first_name']
    l_name = request.form['last_name']
    member_no = request.form['member_no']
    phone_no = request.form['phone_no']
    address = request.form['address']
    new_member = Member(f_name, l_name, member_no, phone_no, address)
    if new_member.f_name is not None and new_member.l_name is not None and new_member.member_no\
            is not None and len(new_member.member_no) == 10 and new_member.phone_no is not None\
            and len(new_member.phone_no) == 10\
            and new_member.address is not None:
        check_member = get_db().verify_member(new_member)
        if check_member is False:
            get_db().insert_member(new_member)
            return redirect('/')
        else:
            return render-template('ajouter-membre.html', erreur="erreur d'ajout")
    else:
        return render_template('ajouter-membre.html', erreur="erreur d'ajout")


@app.route('/membres')
def members_list():
    members = get_db().get_all_members()
    return render_template('membres.html', title='Liste', members=members)
