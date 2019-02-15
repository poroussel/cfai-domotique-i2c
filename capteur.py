# -*- coding: utf-8 -*-

import socket
import struct
import time

from logging import getLogger
logger = getLogger(__name__)

class Capteur(object):
    def __init__(self, name, conf):
        self.name = name
        self.conf = conf

    def read(self, srv):
        raise NotImplementedError


class CapteurI2C(Capteur):
    def read(self, srv):
        return srv.bus.read(self.name)


class CapteurModBUS(Capteur):
    last_seen = None
    
    def read(self, srv):
        SEND_READ = struct.pack("BBBBBBBBBBBB", 0, 0, 0, 0, 0, 6, self.conf["slave"], 0x3, 0x80, 0x00, 0x0, 0xA,);

        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            connection.connect((self.conf["tcp"], self.conf["port"]))
        except:
            return None

        connection.send(SEND_READ)
        RCV = connection.recv(64)
        RCV = struct.unpack('B' * 29, RCV)
        connection.close()
    
        P_BADGE = RCV[9]
        ID_BADGE = RCV[13]

        # Un tag RFID a été lu
        if P_BADGE:
            if ID_BADGE == self.last_seen:
                logger.info("Tag deja vu")
                return None
            self.last_seen = ID_BADGE
            logger.info('Nouveau tag : {}'.format(ID_BADGE))
            return ID_BADGE
        
        return None
    
