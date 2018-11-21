from functools import wraps
from flask import render_template, Response, session, request
from .language.page_401 import *

"""
class Authentication:

    def __init__(self):
        pass

    def is_authenticated(self, session):
        return "id" in session

    def send_unauthorized(self):
        return Response(render_template('401.html'), 403, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    
    def authentication_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not is_authenticated(session):
                return send_unauthorized()
            return f(*args, **kwargs)

        return decorated
     
    def authentication_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not self.is_authenticated(session):
                return self.send_unauthorized()
            return f(*args, **kwargs)

        return decorated
"""


def is_authenticated(session):
    return "id" in session


def send_unauthorized():
    lang = request.cookies.get('lang')
    if lang == 'english':
        text_content = page_401_content_en
    else:
        text_content = page_401_content_fr
    return Response(render_template('401.html', text=text_content), 403, {'WWW-Authenticate': 'Basic realm="Login Required"'})


"""
def authentication_required(self, f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return send_unauthorized()
        return f(*args, **kwargs)

    return decorated
 """


def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return send_unauthorized()
        return f(*args, **kwargs)
    return decorated