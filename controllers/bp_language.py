from flask import Blueprint, make_response, request, redirect

language_bp = Blueprint('set_to_english', __name__)


@language_bp.route('/language')
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
        response.set_cookie("lang", "english")
    return response
