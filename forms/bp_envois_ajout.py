from flask import Blueprint, request, redirect, render_template, g, session
import re
from member import Member
from authentication import authentication_required
from database.queries.Member_queries import MemberQueries
from language.ajouter_membre import *

envois_ajout_bp = Blueprint('add_member_send', __name__)


@envois_ajout_bp.route('/envois_ajout', methods=['POST'])
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
    if session["level"] == 4:
        committee = request.form['committee']
    else:
        committee = session["committee"]

    address = validation_address(apt, postal_code, city, state, country)

    new_member = Member(f_name, l_name, member_no, phone_no, mem_exp_date,
                        reach_moment, birth_date, email, last_donation,
                        date_last_donation, donation_ok, election_year,
                        comment, address, committee)

    text_content = set_text_content()

    if valide_null_membre(new_member) is True:
        check_member = get_db().verify_member(new_member)
        if check_member is False:
            if get_db().verify_member_no(member_no):
                get_db().insert_member(new_member)
                return redirect('/')
            else:
                return render_template("ajouter_membre.html", error="member_no", text=text_content)
        else:
            return render_template('ajouter_membre.html', error="add_error", text=text_content)
    else:
        return render_template('ajouter_membre.html', error="add_error", text=text_content)


def validation_address(apt, postal_code, city, state, country):
    address = ""
    if apt != "":
        address += apt + "," + postal_code + "," + city + "," + state + "," + country
    else:
        address += postal_code + "," + city + "," + state + "," + country

    return address


def valide_null_membre(new_member):
    regex = '^\d+(\.\d*)?|\.\d+'
    user_valide = False
    if new_member.f_name is not None and new_member.l_name is not None and new_member.member_no \
            is not None and new_member.phone_no is not None and new_member.address is not None \
            and new_member.email is not None and new_member.last_donation is not None \
            and new_member.date_last_donation is not None \
            and new_member.committee is not None \
            and len(new_member.member_no) == 10 \
            and len(new_member.phone_no) == 10 \
            and re.match(regex, new_member.last_donation):
        user_valide = True
        return user_valide
    else:
        return user_valide


def set_text_content():
    if request.cookies.get('lang') == 'english':
        text_content = ajouter_membre_content_en
    else:
        text_content = ajouter_membre_content_fr
    return text_content


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = MemberQueries()
    return g._database
