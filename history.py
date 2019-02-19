# -*- coding: utf-8 -*-

import psycopg2
import logging
logging.basicConfig(level=logging.INFO)

from config import CONFIG


class History(object):
    """
    Classe permettant la connexion à la base d'historisation
    des données et l'insertion d'enregistrements
    """
    def __init__(self):
        self.m_connexion = None

    def connexion(self):
        try:
            self.m_connexion = psycopg2.connect(**CONFIG['history-db'])
        except:
            logging.exception('Connexion history-db')
            return False
        return True

    def deconnexion(self):
        if self.m_connexion:
            self.m_connexion.close()

    def write(self, name, value):
        with self.m_connexion:
            with self.m_connexion.cursor() as cur:
                cur.execute('INSERT INTO history (name, value) VALUES (%s, %s)', (name, value))

if __name__ == '__main__':
    srv = History()
    if srv.connexion():
        srv.write('capteur', 'valeur')
        srv.write('capteur', 27)
        srv.write('capteur', 37.2)
        srv.deconnexion()
