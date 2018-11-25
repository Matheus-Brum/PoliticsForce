from flask import Blueprint, request, redirect, render_template, g
import re
from ..member import Member
from ..authentication import authentication_required
from ..database import Database

envois_modification_bp = Blueprint('alter_member_send', __name__)

@envois_modification_bp.route('/envois_modification', methods=['POST'])
@authentication_required
def alter_mmember_send():
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
    circonscription = request.form['circonscription']


    pass