# -*- coding: utf-8 -*-

import sys
import csv
import random
import os.path
import psycopg2
import psycopg2.extras
import logging
logging.basicConfig(level=logging.INFO)

from config import CONFIG
from datetime import date

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

    def write(self, name, value, tm=None):
        with self.m_connexion:
            with self.m_connexion.cursor() as cur:
                if tm is None:
                    cur.execute('INSERT INTO history (name, value) VALUES (%s, %s)', (name, value))
                else:
                    cur.execute('INSERT INTO history (name, value, tmstamp) VALUES (%s, %s, %s)', (name, value, tm))

    def export(self, day):
        if 'history-export-dir' in CONFIG:
            filename = os.path.join(CONFIG['history-export-dir'], 'values-{}.csv'.format(day))
            with self.m_connexion:
                with self.m_connexion.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                    cur.execute('select * from history where date(tmstamp) = %s', (day,))
                    rows = cur.fetchall()
                    with open(filename, 'w') as f:
                        w = csv.DictWriter(f, ['id', 'tmstamp', 'name', 'value'], delimiter=';', lineterminator='\n')
                        w.writeheader()
                        w.writerows(rows)
                    logging.info('Donnees exportees')
        else:
            logging.error('history-export-dir not defined')

if __name__ == '__main__':
    srv = History()
    if srv.connexion():
        if '-t' in sys.argv:
            srv.write('capteur', 'valeur')
            srv.write('capteur', 27)
            srv.write('capteur', 37.2)

        if '-e' in sys.argv:
            srv.export(date.today())

        srv.deconnexion()
