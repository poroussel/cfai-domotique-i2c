# -*- coding: utf-8 -*-

import smbus
import time

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
        self.bus = smbus.SMBus(CONFIG['i2c-bus'])

    def cmd(self, name):
        prm = CONFIG['commands'].get(name, None)
        if prm:
            addr = prm['i2c-addr']
            numc = prm['cmd']
            self.bus.write_byte_data(addr, numc, 150)
        
    def write(self, hw, value):
        hw = CONFIG['hardware'].get(hw, None)
        if hw is None:
            return
        if hw['action'] != 'write':
            return
        self.bus.write_i2c_block_data(hw['i2c-addr'], 7, [int(hw['pin']), int(value)])


    def read(self, hw):
        hw = CONFIG['hardware'].get(hw, None)
        if hw is None:
            return
        if hw['action'] != 'read':
            return
        self.bus.write_byte_data(hw['i2c-addr'], 8, hw['pin'])
        time.sleep(0.05)
        return self.bus.read_byte(hw['i2c-addr'])


if __name__ == "__main__":
    bus = BusI2C()
    bus.cmd('beep')
    
