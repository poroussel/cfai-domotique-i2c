# -*- coding: utf-8 -*-

import time
from mock import Mock

from logging import getLogger
logger = getLogger(__name__)

from config import CONFIG

"""
Communication avec l'arduino

Les commandes définies :

   9 : beep (duree en parametre)
   8 : stockage du valeur d'une pin (n° en parametre) pour lecture
   7 : ecriture d'une valeur

Avant de lire une valeur avec readNumber on doit donc
envoyer la commande 8 suivi du numéro de pin sur lequel
le capteur est connecté.
"""

class BusI2C(object):
    def __init__(self):
        try:
            import smbus
            self.bus = smbus.SMBus(CONFIG['i2c-bus'])
        except (ImportError, IOError):
            logger.exception(CONFIG['i2c-bus'])
            logger.info('Mocking up a bus')
            self.bus = Mock()
            self.bus.read_byte.return_value = 24

    def cmd(self, name):
        prm = CONFIG['commands'].get(name, None)
        if prm:
            addr = prm['i2c-addr']
            numc = prm['cmd']
            self.bus.write_byte_data(addr, numc, 150)

    def write(self, hw, value):
        """
        Lors de l'utilisation de write_block_data le client reçoit
          * num cmd
          * nbre data
          * data 0
          * data 1
          * etc

        La ligne self.bus.write_block_data(hw['i2c-addr'], 4, [11, 22]) génère donc
        du côté arduino : 4 / 2 / 11 / 22. On aura donc cmd = 4, args[0] = 2, etc...
        """
        logger.debug('write {} {}'.format(hw, value))
        hw = CONFIG['hardware'].get(hw, None)
        if hw is None:
            return
        if hw['action'] != 'write':
            return
        try:
            if hw['type'] == 'bool':
                if int(value) == 0:
                    logger.debug('digital addr {} / pin {} / {}'.format(hw['i2c-addr'], int(hw['pin']), 'off'))
                    self.bus.write_block_data(hw['i2c-addr'], 5, [int(hw['pin']), 0])
                else:
                    logger.debug('digital addr {} / pin {} / {}'.format(hw['i2c-addr'], int(hw['pin']), 'on'))
                    self.bus.write_block_data(hw['i2c-addr'], 5, [int(hw['pin']), 1])
            else:
                logger.debug('analog addr {} / pin {} / {}'.format(hw['i2c-addr'], int(hw['pin']), int(value)))
                self.bus.write_block_data(hw['i2c-addr'], 4, [int(hw['pin']), int(value)])
        except:
            logger.exception('error writing {} on {}'.format(value, hw))

    def read(self, hw):
        logger.debug('read {}'.format(hw))
        hw = CONFIG['hardware'].get(hw, None)
        if hw is None:
            return
        if hw['action'] != 'read':
            return
        try:
            self.bus.write_byte_data(hw['i2c-addr'], 8, hw['pin'])
            time.sleep(0.10)
            val = self.bus.read_byte(hw['i2c-addr'])
        except:
            logger.exception('error while reading {}'.format(hw))
            val = -1
        return val


if __name__ == "__main__":
    bus = BusI2C()
    bus.cmd('beep')
