# -*- coding: utf-8 -*-

import smbus
from config import CONFIG
import time

def test():
    bus = smbus.SMBus(1)

    # This is the address we setup in the Arduino Program
    address = 0x04

    def writeNumber(value):
        # bus.write_byte(address, value)
        bus.write_byte_data(address, value, 120)

    def readNumber():
        return bus.read_byte(address)

    
    while True:
        var = input("Enter number (1 - 255) : ")
        if not var:
            continue
    
        writeNumber(var)
        print "RPI: Hi Arduino, I sent you ", var
    
        time.sleep(0.1)
    
        number = readNumber()
        print "Arduino: Hey RPI, I received a digit ", number
        print
    

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
        self.bus.write_byte_data(hw['i2c-addr'], 7, hw['pin'])


    def read(self, hw):
        hw = CONFIG['hardware'].get(hw, None)
        if hw is None:
            return
        if hw['action'] != 'read':
            return
        self.bus.write_byte_data(hw['i2c-addr'], 8, hw['pin'])
        time.sleep(0.1)
        return self.bus.read_byte(hw['i2c-addr'])

if __name__ == "__main__":
    test()
    
