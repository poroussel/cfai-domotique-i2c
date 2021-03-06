# -*- coding: utf-8 -*-

import sys
import select
import argparse
import logging
import time
import json
import requests

import tornado.ioloop
import tornado.web

from config import CONFIG
from camera import VideoCapture
from utils import sendmail

FORMAT = "%(asctime)s %(levelname)s:%(name)s:%(lineno)d : %(message)s"

if CONFIG['logfile']:
    logging.basicConfig(format=FORMAT, filename=CONFIG['logfile'], level=eval('logging.{}'.format(CONFIG['loglevel'])))
else:
    logging.basicConfig(format=FORMAT, level=eval('logging.{}'.format(CONFIG['loglevel'])))

from creation_BDD import create_bdd
from Ypareo import Ypareo
from i2c import BusI2C
from history import History

class Server(object):
    def __init__(self):
        self.bus = BusI2C()
        self.ypareo = Ypareo()
        self.history = History()
        self.collector_url = CONFIG.get('collector-url', None)

        if CONFIG.get('capture', False):
            self.camera = VideoCapture()
        else:
            self.camera = None

        if self.ypareo.connexion():
            logging.info('Connexion Ypareo ok')
        else:
            logging.error('Erreur connexion ypareo')
            self.ypareo = None

        if self.history.connexion():
            logging.info('Connexion History ok')
        else:
            logging.error('Erreur connexion History')
            self.history = None

        self.commands = CONFIG.get('commands', {}).keys()

        logging.info('Initialisation terminée...')
        # Liste des capteurs que l'on doit lire
        self.inputs = {name: conf['class'](name, conf) for name, conf in CONFIG['hardware'].iteritems() if conf['action'] == 'read'}

    def hardware(self, name=None):
        if name:
            return CONFIG['hardware'][name]
        return CONFIG['hardware'].keys()

    def handle_input(self, occupation):
        for cpt, obj in self.inputs.iteritems():
            conf = CONFIG['hardware'][cpt]


            val = obj.read(self)
            if val is None:
                continue

            logging.info('Lecture {} : {}'.format(cpt, val))

            if self.history and conf.get('history', False):
                self.history.write(cpt, str(val))

            if self.collector_url and 'collector-id' in conf:
                logging.debug("Envoi de la valeur vers le collecteur")
                requests.post(self.collector_url, data={'sensor': conf['collector-id'], 'value': val})

            for act in conf.get('execute', []):
                op = act.get('operation', None)
                level = act.get('level', None)
                run = act.get('run', None)
                ocpt = act.get('occupation', None)

                # Si un niveau d'occupation est défini pour la tâche il doit
                # être égal à l'occupation actuelle pour que la tâche soit
                # exéutée.
                if not ocpt is None and ocpt != occupation:
                    logging.debug('Occupation incoherente avec celle de la tâche')
                    continue

                # Si la tâche n'est pas correctement configurée on passe à la suivante
                if op is None or level is None or run is None:
                    logging.error('Configuration action incomplète')
                    continue

                # Si la condition de déclenchement est valide on lance la routine
                if op(val, level):
                    logging.debug(' --> exécution de {}'.format(run))
                    if run == 'capture':
                        self.camera.capture()
                    elif run == 'write':
                        hardware = act.get('hardware', None)
                        value = act.get('value', None)
                        if hardware is None or value is None:
                            logging.error('Action écriture incomplète')
                        else:
                            logging.info('Envoi de {} sur {}'.format(value, hardware))
                            self.bus.write(hardware, value)
                    elif run == 'email':
                        logging.info('Envoi email')
                        try:
                            sendmail(CONFIG['to_addr'], act.get('subject', 'Empty'), act.get('body', 'Empty'))
                        except:
                            logging.error('Erreur envoi email')
                    elif run in self.commands:
                        logging.info('Lancement commande {}'.format(run))
                        self.bus.cmd(run)
                    else:
                        logging.error('Tâche {} inconnue'.format(run))

            time.sleep(0.1)


def console_server(server):
    logging.info('Lancement du serveur...')
    loop = True
    inl = [sys.stdin]
    while loop:
        try:
            readable, _, _ = select.select(inl, [], [], CONFIG['temporisation'])

            # Sortie par timeout, on effectue les traitements récurrents
            if not readable:
                occupation = False
                # Détermination de l'occupation des locaux
                if server.ypareo:
                    try:
                        planning = server.ypareo.interroPlanning()
                        occupation = len(planning) > 0
                    except:
                        logging.exception('Lecture planning')

                # La valeur calculée peut être écrasée par une clé du fichier de configuration
                if not CONFIG.get('force-occupation', None) is None:
                    occupation = CONFIG['force-occupation']

                server.handle_input(occupation)
            else:
                for h in readable:
                    if h == sys.stdin:
                        line = sys.stdin.readline()

        except KeyboardInterrupt:
            logging.info('Interruption clavier')
            loop = False

    server.ypareo.deconnexion()
    logging.info('Fermeture du serveur')



def web_server(server):
    logging.info('Lancement du serveur web...')


    def callback():
        server.handle_input(False)

    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.write('Yo !')

    class Hardware(tornado.web.RequestHandler):
        def get(self):
            self.write(json.dumps(server.hardware(), indent=4))

    class HardwareByName(tornado.web.RequestHandler):
        def get(self, name):
            filtered = {k:v for k, v in server.hardware(name).iteritems() if type(v) in [str, unicode, int, float]}
            self.write(json.dumps(filtered, indent=4))

    app = tornado.web.Application([
        (r"/hardware/([a-z]+)", HardwareByName),
        (r"/hardware", Hardware),
        (r"/", MainHandler),
    ])
    app.listen(8888, '0.0.0.0')

    tornado.ioloop.PeriodicCallback(callback, CONFIG['temporisation'] * 1000).start()
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--run', action='store_true', default=False, help=u"Lancement serveur")
    parser.add_argument('-w', '--web', action='store_true', default=False, help=u"Lancement serveur web")
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
        console_server(Server())
    elif env.web:
        web_server(Server())
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
