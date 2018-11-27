# coding=utf-8
from .layout import *

# en = {**page_en, **Layout.en}
# en = page_en.update(Layout.en)

accueil_fr = {
    "title_tab": "Bienvenu(e)!",
    "make_account": "Cliquez ici pour créer un compte",
    "connected_as": "Vous êtes connecté(e) en tant que",
    "disconnect": "Se déconnecter",
    "not_connected": "Vous n'êtes pas connecté(e).",
    "e-mail": "Courriel :",
    "password": "Mot de passe :",
    "btn_reset": "Vider",
    "btn_submit": "Se connecter",
    "email_pass": "Le email ou le mot de passe sont incorrectes!",
    "mandatory": "Tous les champs sont obligatoires. Recommencez."
}
accueil_content_fr = {**accueil_fr, **layout_fr}

accueil_en = {
    "title_tab": "Welcome!",
    "make_account": "Click here to create an account",
    "connected_as": "You are logged in as",
    "disconnect": "Sign out",
    "not_connected": "You are not logged in.",
    "e-mail": "E-mail :",
    "password": "Password :",
    "btn_reset": "Reset",
    "btn_submit": "Sign in",
    "email_pass": "Email or password is incorrect!",
    "mandatory": "All fields are mandatory. Please start again."
}
accueil_content_en = {**accueil_en, **layout_en}
