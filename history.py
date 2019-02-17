# -*- coding: utf-8 -*-

import datetime
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
        self.m_cursor = None

    def connexion(self):
        try:
            import psycopg2
            self.m_connexion = psycopg2.connect(**CONFIG['history-db'])
            self.m_cursor = self.m_connexion.cursor()
        except:
            logging.exception('Connexion history-db')
            return False
        return True

    def deconnexion(self):
        if self.m_connexion:
            self.m_connexion.close()

    def write(self, name, value):
        pass


if __name__ == '__main__':
    srv = History()
    if srv.connexion():
        srv.deconnexion()
