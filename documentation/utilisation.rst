================================
Utilisation du serveur domotique
================================

Installation
============

Configuration
=============

La configuration du serveur est stockée dans un dictionnaire python
nommé `CONFIG` dans le fichier `config.py`. Ce dictionnaire est importé
dans les différents fichiers utilisant un paramètre de configuration.

A chaque clé est associé soit une valeur (chaîne de caractères, nombre, booléen)
ou un sous-dictionnaire. Voici une liste des différentes clés par catégorie.

Base de données
---------------

* `sqlite-path` : nom du fichier pour la base de données locale
* `ypareo-db` : accès au serveur de base de données Ypareo

  - `database` : nom de la base
  - `user` : utilisateur de connexion
  - `password` : mot de passe
  - `host` : nom ou adresse ip de la machine hôte
  - `port` : port de connexion

Périphériques
-------------


Email
-----

* `smtp` : configuration du serveur smtp pour l'envoi d'emails
  
  - `host` : nom du serveur (ex: smtp.free.fr)
  - `port` : port de connexion (25)
  - `username` : nom d'utilisateur
  - `password` : mot de passe
  - `starttls` : utilisation de tls (True ou False)

Autres
------

* `i2c-bus` : numéro du bus i2c à utiliser
* `temporisation` : délai en secondes entre deux lectures de données
* `loglevel` : niveau d'information dans le log (ERROR, INFO ou DEBUG)
* `logfile` : nom du fichier log ou None pour utiliser la console


    
Exemples de commandes
=====================

Lecture à intervalle régulier (0.1s) d'un capteur ::

  watch -d -n 0 python server.py -rv capteur

