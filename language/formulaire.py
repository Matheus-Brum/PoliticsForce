# coding=utf-8
from .layout import *

formulaire_fr = {
    "page_title": "Création d'un compte",
    "password_requires": "Erreur: Votre mot de passe doit contenir une lettre majuscule, un caractère spécial, "
                         "un chiffre et 8 caractères.",
    "mandatory": "Tous les champs sont obligatoires. Recommencez.",
    "username": "Nom d'utilisateur",
    "password": "Mot de passe",
    "btn_reset": "Vider",
    "btn_submit": "Soumettre"
}
formulaire_content_fr = {**formulaire_fr, **layout_fr}

formulaire_en = {
    "page_title": "Create an account",
    "password_requires": "Error: Your password must contain a capital letter, a special character, a number and "
                         "8 characters.",
    "mandatory": "All fields are mandatory. Please start again.",
    "username": "Username",
    "password": "Password",
    "btn_reset": "Reset",
    "btn_submit": "Submit"
}
formulaire_content_en = {**formulaire_en, **layout_en}
