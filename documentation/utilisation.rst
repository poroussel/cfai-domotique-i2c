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
soit un sous-dictionnaire. Voici une liste des différentes clés par catégorie.

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

Les différents périphériques (capteurs et actionneurs) utilisables par le serveur domotique sont
déclarés sous la forme d'un dictionnaire sous la clé `hardware`. Par exemple pour un capteur de
température la configuration pourrait être :

.. code:: python

  "hardware": {
      "temp": {
          "label": "Température cuisine",
	  "action": "read",
	  "type": "float",
	  "i2c-addr": 4,
	  "pin": 0,
	  "execute": []
      },
  }

Chaque périphérique doit porter au minimum les informations suivantes :

* `label` : description du périphérique
* `action` : capteur ou actionneur (`read` ou `write`)
* `type` : type de valeur (`float`, `bool`)
* `i2c-addr` : adresse du contrôleur arduino sur le bus i2c
* `pin` : numéro du pin que lequel est connecté le périphérique

À chaque capteur peut être associé une liste de tâches à effectuer si une condition est vérifiée. La
liste est définie sous la clé `execute`, chaque élément de la liste étant un dictionnaire comportant au
minimum 3 clés :

* `operation` : la fonction déterminant si la tâche doit être exécutée
* `level` : la valeur envoyée en paramètre à la fonction en plus de la valeur retournée par le capteur
* `run` : la tâche à exécuter (`capture`, `write`, `email`)

Si la clé `occupation` (`True` ou `False`) est présente la tâche sera exécutée uniquement si l'occupation
des salles calculée à partir du planning est égale à la valeur associée à cette clé.

Signification des tâches :

* `capture` : enregistrement d'une séquence vidéo
* `write` : envoi d'un valeur sur un périphérique (`hardware` et `value` en clés supplémentaires)
* `email` : envoi d'un email (`subject` et `body` en clés supplémentaires)

Par exemple, avec la configuration ci-dessous, l'actionneur `lumiere` sera passé à 1, et donc la
lumière allumée, dès que le capteur `temp` retourne une valeur inférieure ou égale à 120.

.. code:: python

  "hardware": {
      "lumiere": {
          "label": "Eclairage interieur",
          "action": "write",
          "type": "bool",
          "i2c-addr": 4,
          "pin": 10,
      },
      "temp": {
          "label": "Température cuisine",
	  "action": "read",
	  "type": "float",
	  "i2c-addr": 4,
	  "pin": 0,
	  "execute": [
                {
                    "operation": operator.le,
                    "level": 120,
                    "run": "write",
                    "hardware": "lumiere",
                    "value": 1,
                },
	  ]
      },
  }

`operator.le` correspond à la fonction `le` (Less or Equal) définie dans le module standard `operator`. Cette fonction
attend en paramètre 2 valeurs et retourne `True` si et seulement si la premiere valeur est inférieure ou égale à la
seconde. Ce module propose d'autres opérateurs de comparaison utilisables dans le fichier de configuration. Il doit
être importé dans le fichier de configuration.

Email
-----


* `smtp` : configuration du serveur smtp pour l'envoi d'emails

  - `host` : nom du serveur (ex: smtp.free.fr)
  - `port` : port de connexion (25)
  - `username` : nom d'utilisateur
  - `password` : mot de passe
  - `starttls` : utilisation de tls (True ou False)
  - `from_addr` : adresse email de l'envoyeur

* `to_addr` : adresse email du destinataire

Autres
------

* `i2c-bus` : numéro du bus i2c à utiliser
* `temporisation` : délai en secondes entre deux lectures de données
* `capture` : utilisation de la camera liée à la Raspberry (True ou False)
* `loglevel` : niveau d'information dans le log (ERROR, INFO ou DEBUG)
* `logfile` : nom du fichier log ou None pour utiliser la console
* `force-occupation` : permet de définir si les locaux sont occupés ou pas quelque soit le contenu de la base de données (True ou False)


Exemples de commandes
=====================

Affichage de l'aide ::

  python server.py -h

Lecture à intervalle régulier (0.1s) d'un capteur ::

  watch -d -n 0 python server.py -rv capteur

Liste des périphériques définis dans le fichier de configuration ::

  python server.py --list

Affichage de la valeur retournée par un capteur ::

  python server.py --read capteur

Envoi d'une valeur à un actionneur ::

  python server.py --write lumiere 1

Lancement du serveur ::

  python server.py --run
