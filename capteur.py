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
    BUFFER_SIZE = 100

    def __init__(self, name, conf):
        Capteur.__init__(self, name, conf)
        self.last_value = None
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.conf["tcp"], self.conf["port"]))
            req = struct.pack('BBBBBBBBBBB', 0, 0, 0, 0, 0, 5, 0xff, 0x2b, 0x0e, 0x03, 0x00)
            self.connection.send(req)
            self.connection.recv(self.BUFFER_SIZE)
            logger.info('Identification OsiTrack')
        except:
            self.connection = None
            logger.exception('Connection error')
        

    def read(self, srv):
        if self.connection is None:
            return None
        
        req = struct.pack('BBBBBBBBBBBB', 0, 0, 0, 0, 0, 6, self.conf['slave'], 0x03, 0x80, 0x00, 0x00, 0x10)
        self.connection.send(req)
        rec = self.connection.recv(self.BUFFER_SIZE)
        
        tr_id = struct.unpack('>H', rec[0:2])[0]
        proto = struct.unpack('>H', rec[2:4])[0]
        length = struct.unpack('>H', rec[4:6])[0]
        unit = struct.unpack('B', rec[6])[0]
        function = struct.unpack('B', rec[7])[0]
        data = rec[8:]

        # Si la réponse vient du bon esclave et la bonne fonction
        if unit == self.conf['slave'] and function == 3:
            values = [struct.unpack('B', d)[0] for d in data]
            if values[1] == 1:
                compteur = values[3:5]
                identifiant = values[5:20]
                if identifiant != self.last_value:
                    self.last_value = identifiant
                    return identifiant
        
        return None
