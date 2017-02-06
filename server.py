# -*- coding: utf-8 -*-

import sys
import select
import argparse
import logging
import time

from config import CONFIG

FORMAT = "%(asctime)s %(levelname)s:%(name)s:%(lineno)d : %(message)s"

if CONFIG['logfile']:
    logging.basicConfig(format=FORMAT, filename=CONFIG['logfile'], level=eval('logging.{}'.format(CONFIG['loglevel'])))
else:
    logging.basicConfig(format=FORMAT, level=eval('logging.{}'.format(CONFIG['loglevel'])))

from creation_BDD import create_bdd
from Ypareo import Ypareo
from i2c import BusI2C

class Server(object):
    def __init__(self):
        self.bus = BusI2C()
        self.ypareo = Ypareo()

        if not self.ypareo.connexion():
            logging.error('Erreur connexion ypareo')

        # Liste des capteurs que l'on doit lire
        self.inputs = [name for name, conf in CONFIG['hardware'].iteritems() if conf['action'] == 'read']

    def handle_input(self):
        for cpt in self.inputs:
            conf = CONFIG['hardware'][cpt]
            val = self.bus.read(cpt)
            if val < 0:
                continue
            
            print 'Lecture {} : {}'.format(cpt, val)
            for act in conf.get('execute', []):
                op = act['operation']
                level = act['level']
                run = act['run']
                print act
                
            time.sleep(0.1)
        
    def run(self):
        logging.info('Lancement du serveur...')
        loop = True
        inl = [sys.stdin]
        while loop:
            try:
                readable, _, _ = select.select(inl, [], [], CONFIG['temporisation'])

                # Sortie par timeout
                if not readable:
                    try:
                        planning = self.ypareo.interroPlanning()
                    except:
                        logging.exception('Lecture planning')
                    self.handle_input()
                else:
                    for h in readable:
                        if h == sys.stdin:
                            line = sys.stdin.readline()
                    
            except KeyboardInterrupt:
                logging.info('Interruption clavier')
                loop = False

        self.ypareo.deconnexion()
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
        Server().run()
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
            
