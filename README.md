# Atelier_politique

## Description

Ce programme est une platforme qui permet de bien gérer un commité ou
un parti politique.

## Attention
Les usernames et les mots de passe des utilisateurs sont dans le fichier db/reset_and_populate.sql.
Je vous suggère de vous logger en tant que admin. Donc, username = 'admin' et mot de passe = 'admin123'.

## Compilation sous Linux

Pour compiler le programme sous linux il suffit de taper la commande suivante dans le repertoir ou ce trouve le projet:

~~~
$ cd repertoire du projet
$ make
~~~

puis copier le url et essayer avec n'importe quelle browser.

## Compilation sous Windows

Pour compiler le programme sous windows il suffit de taper les commande suivante dans le repertoir ou ce trouve le projet:

~~~
cd repertoire du projet
set FLASK_APP=index.py
flask run
~~~

puis copier le url et essayer avec n'importe quelle browser.

## Dependances

flask, sqlite3
