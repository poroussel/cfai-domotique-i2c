=====================================
Architecture matérielle et logicielle
=====================================

Le système est basé sur une application maître installée sur un ordinateur Raspberry
qui contrôle des périphériques (capteurs et actionneurs) à travers des microcontrôleurs
Arduino. Un bus i2c relie la Raspberry et le(s) Arduino(s).

Le logiciel installé sur les Arduinos est générique, il ne dépend pas des périphériques
attachés. Ces périphériques sont simplement décrits dans le fichier de configuration
de l'application serveur installée sur la Raspberry.

Les pins n° 10, 11, 12 et 13 sont configurés en sorties digitales.


Protocole de communication
==========================

Le client Arduino reçoit des commandes en écriture ou des requêtes de lecture
sur le bus i2c. Chaque commande est composée d'une suite d'octets dont le premier
défini le n° de la commande. Les commandes existantes sont les suivantes (valeurs
complémentaires entre parenthèses) :

* 1 : reset du microcontrôleur
* 2 : beep si buzzer connecté sur le pin 9
* 4 : écriture d'un entier entre 0 et 255 (nombre paramètres | n° pin | valeur)
* 5 : écriture d'un booléen 0 ou 1 (nombre paramètres | n° pin | valeur)
* 8 : stockage de la valeur d'un capteur pour lecture (n° pin)

La lecture de la valeur d'un capteur s'effectue donc en 2 temps :

* envoi de la commande 8 identifiant le n° de pin dont on veut lire la valeur
* envoi d'une requête de lecture qui retourne la valeur stockée par la commande 8

Communication entre les matériels
=================================

Sur un bus i2c chaque esclave doit déclarer son adresse, adresse qui sera utilisée par
le maître pour l'envoi de commandes.


Librairie Arduino Wire
----------------------

La librairie Wire permet d'utiliser les capacités de communication
i2c des Arduinos.

https://www.arduino.cc/en/Reference/Wire

et

http://playground.arduino.cc/Main/WireLibraryDetailedReference


Librairie python smbus
----------------------

Du côté Raspberry la communication i2c est gérée à l'aide de la
bibliothèque smbus.


Informations sur le bus i2c
---------------------------

Sur la Raspberry la commande `i2cdetect -l` permet de lister les bus i2c présents sur la machine.
Une fois le bus identifié il est possible de lister les esclaves présents sur le bus à l'aide
de la commande `i2cdetect n°bus`.


Utilisation des données du planning
===================================

La base de données `Ypareo` est consultée régulièrement pour déterminer si une occupation des salles
est prévue dans la journée. Si le nombre de réservation de salle est supérieur à 0 on considère que
les locaux sont occupés.
