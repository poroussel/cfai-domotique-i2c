# -*- coding: utf-8 -*-

import sys
import select
import logging
logging.basicConfig(level=logging.INFO)

from config import CONFIG
from creation_BDD import create_bdd
from Ypareo import Ypareo
from i2c import BusI2C

def serve():
    bus = BusI2C()
    ypareo = Ypareo()

    if not ypareo.connexion():
        logging.error('Erreur connexion ypareo')

    loop = True    
    inl = [sys.stdin]

    logging.info('Lancement du serveur...')
    while loop:
        try:
            readable, _, _ = select.select(inl, [], [], CONFIG['frequence'])

            # Sortie par timeout
            if not readable:
                try:
                    planning = ypareo.interroPlanning()
                except:
                    logging.exception('Lecture planning')
            else:
                for h in readable:
                    if h == sys.stdin:
                        line = sys.stdin.readline()
                    
        except KeyboardInterrupt:
            logging.info('Interruption clavier')
            loop = False
    logging.info('Fermeture du serveur')
    
if __name__ == "__main__":
    if '--build' in sys.argv:
        print 'Creation de la base de données locale...'
        create_bdd()
        print '...terminé'
    elif '--run' in sys.argv:
        serve()
    elif '--beep' in sys.argv:
        BusI2C().cmd('beep')
    elif '--cmd' in sys.argv:
        BusI2C().cmd(sys.argv[sys.argv.index('--cmd') + 1])
    elif '--read' in sys.argv:
        val = BusI2C().read(sys.argv[sys.argv.index('--read') + 1])
        print 'Valeur lue : ', val
    elif '--write' in sys.argv:
        idx = sys.argv.index('--write')
        BusI2C().write(sys.argv[idx + 1], sys.argv[idx + 2])
    else:
        print 'Erreur de parametre'
