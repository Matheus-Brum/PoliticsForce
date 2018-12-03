from flask import Blueprint, request, redirect, g
from ..member import Member
from ..authentication import authentication_required
from database.db_general import Database

envois_modification_bp = Blueprint('alter_member_send', __name__)


@envois_modification_bp.route('/envois_modification', methods=['POST'])
@authentication_required
def alter_member_send():
    f_name = request.form['first_name']
    l_name = request.form['last_name']
    member_no = request.form['member_no']
    phone_no = request.form['phone_no']
    address = request.form['address']
    email = request.form['email']
    last_donation = request.form['last_donation']
    date_last_donation = request.form['last_donation_date']
    donation_ok = request.form['donated']
    election_year = request.form['elec_year']
    mem_exp_date = request.form['expiring_date']
    reach_moment = request.form['reach_day']
    birth_date = request.form['birth_date']
    comment = request.form['comment']
    committee = request.form['committee']
    """
    print(f_name, l_name, member_no, phone_no, address, email, last_donation, date_last_donation,
          donation_ok, election_year, mem_exp_date, reach_moment, birth_date, comment, committee)
    """

    data = [f_name, l_name, member_no, phone_no, address,
            email, last_donation, date_last_donation, donation_ok, election_year,
            mem_exp_date, reach_moment, birth_date, comment, committee]
    if None in data:
        return 'ERROR'
    else:
        member = Member(f_name, l_name, member_no, phone_no, mem_exp_date,
                        reach_moment, birth_date, email, last_donation, date_last_donation,
                        donation_ok, election_year, comment, address, committee)
        get_db().update_member(member)
        return redirect('/modifier_membre/' + member.member_no)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database

