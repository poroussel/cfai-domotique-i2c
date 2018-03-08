# -*- coding: utf-8 -*-

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
        pass
