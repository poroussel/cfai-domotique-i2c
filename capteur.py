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
        logger.info('Capteur {} configuré'.format(name))

    def read(self, srv):
        raise NotImplementedError


class CapteurI2C(Capteur):
    def read(self, srv):
        return srv.bus.read(self.name)


class CapteurModBUS(Capteur):
    def __init__(self, name, conf):
        Capteur.__init__(self, name, conf)
        self.last_value = None
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            connection.connect((self.conf["tcp"], self.conf["port"]))
        except:
            self.connection = None
            logger.error('Connection error')

    def read(self, srv):
        if self.connection:
            SEND_READ = struct.pack("BBBBBBBBBBBB", 0, 0, 0, 0, 0, 6, self.conf["slave"], 0x3, 0x80, 0x00, 0x0, 0xA,)
            connection.send(SEND_READ)
            RCV = connection.recv(64)

            RCV = struct.unpack('B' * 29, RCV)
            P_BADGE = RCV[9]
            ID_BADGE = RCV[13]

            if P_BADGE and ID_BADGE != self.last_value:
                self.last_value = ID_BADGE
                return ID_BADGE
        return None
