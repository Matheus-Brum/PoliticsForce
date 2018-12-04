from ..authentication import authentication_required
from ..database.db_general import Database
from ..language.formulaire import *
from flask import Blueprint, render_template, request, g
import uuid
import hashlib
import re
import random

formulaire_bp = Blueprint('formulaire_creation', __name__)


@formulaire_bp.route('/formulaire', methods=["GET", "POST"])
@authentication_required
def formulaire_creation():
    lang = request.cookies.get('lang')
    pwd = password_generator()
    if lang == 'english':
        text_content = formulaire_content_en
    else:
        text_content = formulaire_content_fr
    if request.method == "GET":
        return render_template("formulaire.html", text=text_content, password=pwd)
    elif request.method == "POST":
        username = request.form["email"]
        password = request.form["password"]

        reg0bool = False
        reg1bool = False
        reg2bool = False
        reg3bool = False

        regex1 = "[A-Z]"
        regex2 = "[0-9]"
        regex3 = "['$', '#', '@', '!', '*']"

        longpass = len(password)

        if username == "" or password == "":
            return render_template("formulaire.html",
                                   error="mandatory", text=text_content, password=pwd)
        else:
            if longpass >=8:
                reg0bool = True
            if re.search(regex1, password) is not None:
                reg1bool = True
            if re.search(regex2, password) is not None:
                reg2bool = True
            if re.search(regex3, password) is not None:
                reg3bool = True

        if reg0bool and reg1bool and reg2bool and reg3bool is True:
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(str(password + salt).encode("utf-8")).hexdigest()
            db = get_db()
            print('username', username)
            print('salt', salt)
            print('hashed', hashed_password)
            if db.validate_user_pass(username, password):
                return render_template("/formulaire.html", error="user_exist", text=text_content, password=pwd)
            else:
                db.create_user(username, salt, hashed_password)

            return render_template("/confirmation.html", password=password)
        else:
            return render_template("formulaire.html",
                                   error="password_requires", text=text_content, password=pwd)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


def password_generator():
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
