# -*- coding: utf-8 -*-

import datetime
import unicodedata
import logging
logging.basicConfig(level=logging.INFO)

from config import CONFIG

code_site_dole = '34863104'
abrege_site_dole = '39D'

class Ypareo(object):
    """
    Classe permettant la connexion et la recuperation
    du planning du serveur Ypareo.
    """
    def __init__(self):
        self.m_connexion = None
        self.m_cursor = None


    def connexion(self):
        """Methode permettant de se connecter au serveur Ypareo, retourne True si etablie et False en cas d'erreur"""

        try:
            import psycopg2
            self.m_connexion = psycopg2.connect(**CONFIG['ypareo-db'])
            self.m_cursor = self.m_connexion.cursor()
        except:
            logging.exception('Connexion postgres')
            return False
        return True

    def deconnexion(self):
        """Methode permettant de se deconnecter du serveur Ypareo"""

        self.m_connexion.close()


    def interroPlanning(self):
        """Methode permettant d'extraire le planning des salles du serveur Ypareo
           et de le retourner dans un dictionnaire"""

        date = datetime.date.today()

        query_salle = """
        SELECT right(nom_salle, -2), min(minute_deb), max(minute_fin) FROM DONNEES
           WHERE abrege_site = '{abrege}' and annee_seance = {annee} and mois_seance = {mois} and jour_seance = {jour}
           GROUP BY nom_salle
        """

        planning = {}
        #recuperation des seances de la journee
        self.m_cursor.execute(query_salle.format(abrege=abrege_site_dole, annee=date.year, mois=date.month, jour=date.day))
        rows = self.m_cursor.fetchall()
        for row in rows:
            planning[row[0]] = {'nom_salle' : row[0].decode('utf-8'), 'etat' : 1, 'debut' : row[1], 'fin' : row[2]}
        return planning


if __name__ == '__main__':
    srv = Ypareo()
    if srv.connexion():
        print srv.interroPlanning()
        srv.deconnexion()
