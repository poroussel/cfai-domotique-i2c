# -*- coding: utf-8 -*-

import sys
import select
import argparse
import logging
from config import CONFIG

logging.basicConfig(level=eval('logging.{}'.format(CONFIG['loglevel'])))

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

    ypareo.deconnexion()
    logging.info('Fermeture du serveur')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--run', action='store_true', default=False, help=u"Lancement serveur")
    parser.add_argument('-b', '--beep', action='store_true', default=False, help=u"Génération d'un bip")
    parser.add_argument('-c', '--create', action='store_true', default=False, help=u"Initialisation de la base locale")
    parser.add_argument('-e', '--execute', default=None, help=u"Exécution d'une commande")
    parser.add_argument('-l', '--list', action='store_true', default=False, help=u"Liste les périphériques définis")
    parser.add_argument('-rv', '--read', metavar='capteur', default=None, help=u"Lecture d'un capteur")
    parser.add_argument('-wv', '--write', metavar=('actionneur', 'valeur'), default=None, help=u"Écriture d'une valeur", nargs=2)
    
    env = parser.parse_args(sys.argv[1:])

    if env.create:
        print 'Creation de la base de données locale...'
        create_bdd()
        print '...terminé'
    elif env.run:
        serve()
    elif env.beep:
        BusI2C().cmd('beep')
    elif env.execute:
        BusI2C().cmd(env.execute)
    elif env.read:
        val = BusI2C().read(env.read)
        print 'Valeur lue pour {} : {}'.format(env.read, val)
    elif env.write:
        BusI2C().write(env.write[0], env.write[1])
    elif env.list:
        print u'Les périphériques définis : '
        print
        for name, conf in CONFIG['hardware'].iteritems():
            print ' * {} : {}'.format(name, conf['label'])
            
