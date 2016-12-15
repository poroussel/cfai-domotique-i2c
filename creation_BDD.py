# -*- coding: utf-8 -*-

import sqlite3
from config import CONFIG

def create_bdd():
    connexion = sqlite3.connect(CONFIG['sqlite-path'])
    curseur = connexion.cursor()


    query = """CREATE TABLE VANNE (code_salle, nom_salle, type, id_v, mode, cons_manuel, niv_utilisation)"""

    query2 = """INSERT INTO VANNE
            VALUES ('34987384', 'informatique industrielle', 1, 2, 1, 15, 1),
                   ('34987384', 'informatique industrielle', 1, 3, 1, 15, 1),
                   ('34987379', 'salle habilitation', 1, 4, 1, 15, 1),
                   ('34987386', 'atelier maintenance', 1, 5, 1, 15, 1),
                   ('34987386', 'atelier maintenance', 1, 6, 1, 15, 1),
                   ('34987386', 'atelier maintenance', 1, 7, 1, 15, 1),
                   ('34987386', 'atelier maintenance', 1, 8, 1, 15, 1),
                   ('34987386', 'atelier maintenance', 1, 9, 1, 15, 1),
                   ('34987386', 'atelier maintenance', 1, 10, 1, 15, 1),
                   ('34987386', 'atelier maintenance', 1, 11, 1, 15, 1),
                   ('34987386', 'atelier maintenance', 1, 12, 1, 15, 1),
                   ('34987382', 'conception mecanique', 1, 13, 1, 15, 1),
                   ('34987382', 'conception mecanique', 1, 14, 1, 15, 1),
                   ('34987382', 'conception mecanique', 1, 15, 1, 15, 1),
                   ('34987382', 'conception mecanique', 1, 16, 1, 15, 1),
                   ('34987367', 'salle ifti', 1, 17, 1, 15, 1),
                   ('34987367', 'salle ifti', 1, 18, 1, 15, 1),
                   ('34987367', 'salle ifti', 1, 19, 1, 15, 1),
                   ('34982558', 'salle 1', 1, 20, 1, 15, 1),
                   ('34982562', 'salle 2', 1, 21, 1, 15, 1),
                   ('34982563', 'salle 3', 1, 22, 1, 15, 1),
                   ('34982564', 'electronique', 1, 23, 1, 15, 1),
                   ('34982564', 'electronique', 1, 24, 1, 15, 1),
                   ('34982567', 'salle 5', 1, 25, 1, 15, 1),
                   ('34982568', 'multimedia', 1, 26, 1, 15, 1),
                   ('34982569', 'salle 6', 1, 27, 1, 15, 1),
                   ('34982569', 'salle 6', 1, 28, 1, 15, 1),
                   ('34982571', 'salle 7', 1, 29, 1, 15, 1),
                   ('34982571', 'salle 7', 1, 30, 1, 15, 1),
                   ('34982580', 'centre de documentation', 1, 31, 1, 15, 1),
                   ('101', 'espace repas formateurs', 2, 32, 1, 15, 1),
                   ('102', 'developpeur', 2, 33, 1, 15, 1),
                   ('103', 'hall', 2, 34, 1, 15, 1),
                   ('103', 'hall', 2, 35, 1, 15, 1),
                   ('104', 'accueil', 2, 36, 1, 15, 1),
                   ('105', 'secretariat de direction', 2, 37, 1, 15, 1),
                   ('106', 'salle des imprimantes', 2, 38, 1, 15, 1),
                   ('107', 'salle formateurs', 2, 39, 1, 15, 1),
                   ('107', 'salle formateurs', 2, 40, 1, 15, 1),
                   ('108', 'bureau formateurs', 2, 41, 1, 15, 1),
                   ('109', 'veranda', 2, 42, 1, 15, 1),
                   ('109', 'veranda', 2, 43, 1, 15, 1),
                   ('34982565', 'salle 4', 1, 44, 1, 15, 1),
                   ('34982565', 'salle 4', 1, 45, 1, 15, 1),
                   ('34982566', 'reunion', 1, 46, 1, 15, 1),
                   ('34982566', 'reunion', 1, 47, 1, 15, 1)"""

    query4 = """SELECT * FROM VANNE"""
    query3 = """DROP TABLE VANNE"""

    #creation de la table SAUVEGARDE
    query5 = """CREATE TABLE SAUVEGARDE (id_v INT, code_salle VARCHAR, consigne INT, date DATE, debut INT, fin INT, etat INT, mode INT, type INT)"""

    query6 = """SELECT * FROM SAUVEGARDE"""
    query7 = """DROP TABLE SAUVEGARDE"""

    curseur.execute(query)
    curseur.execute(query2)
    curseur.execute(query5)
    connexion.commit()
    connexion.close()
