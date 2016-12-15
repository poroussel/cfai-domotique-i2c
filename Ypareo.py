# -*- coding: utf-8 -*-

import psycopg2
import datetime
import unicodedata
from config import CONFIG

code_site_dole = '34863104'
abrege_site_dole = '39D'

class Ypareo:
    """
    Classe permettant la connexion et la recuperation
    du planning du serveur Ypareo.
    """

    database = {
        'database' : 'donneesypareo',
        'user' : 'ypareo',
        'password' : 'ypareo',
        'host' : 'srv-iris-sn',
        'port' : 5432,
    }

    def __init__(self):
        self.m_connexion = None
        self.m_cursor = 0
        self.compteurMail = 0


    def connexion(self):
        """Methode permettant de se connecter au serveur Ypareo, retourne True si etablie et False en cas d'erreur"""
        
        try:
            self.m_connexion = psycopg2.connect(**CONFIG['ypareo-db'])
            self.m_cursor = self.m_connexion.cursor()
        except Exception, e:
            print e
            return False
        return True

    def deconnexion(self):
        """Methode permettant de se deconnecter du serveur Ypareo"""

        self.m_connexion.close()

    
    def interroPlanning(self):
        """Methode permettant d'extraire le planning des salles du serveur Ypareo
           et de le retourner dans un dictionnaire"""

        date = datetime.date.today()
        
        # Pour les tests on choisit une date fixe
        date = datetime.date(2014, 10, 8)


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

