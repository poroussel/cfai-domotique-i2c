# -*- coding: utf-8 -*-

import socket
import struct
import time

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
    def read(self, srv):

        SEND_READ = struct.pack("BBBBBBBBBBBB", 0, 0, 0, 0, 0, 6, self.conf["slave"], 0x3, 0x80, 0x00, 0x0, 0xA,);

        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            connection.connect((self.conf["tcp"], self.conf["port"]))
        except:
            return -1


        connection.send(SEND_READ)

        RCV = connection.recv(64)
            
        RCV = struct.unpack('B' * 29, RCV)
    
        P_BADGE = RCV[9]
        ID_BADGE = RCV[13]
    
        ACCESS = 2
        if P_BADGE and ID_BADGE == 164:
            print "Badge Accepted"
            ACCESS = 1
        elif P_BADGE:
            print "Badge Refused"
            ACCESS = 0
        connection.close()

        return ACCESS
