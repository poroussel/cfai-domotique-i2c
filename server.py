# -*- coding: utf-8 -*-

import sys

from config import CONFIG
from creation_BDD import create_bdd
#from Ypareo import Ypareo
from i2c import BusI2C

def serve():
    bus = BusI2C()
    bus.cmd('beep')
    print bus.read('capteur')
    
    ypareo = Ypareo()

    if not ypareo.connexion():
        print 'Erreur de connexion ypareo, sortie....'
        return

    planning = ypareo.interroPlanning()
    print planning



if __name__ == "__main__":
    if '--build' in sys.argv:
        print 'Creation de la base de données locale...'
        create_bdd()
        print '...terminé'
    elif '--run' in sys.argv:
        print 'Lancement du serveur'
        serve()
    else:
        print 'Erreur de parametre'
