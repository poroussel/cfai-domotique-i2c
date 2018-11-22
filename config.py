# -*- coding: utf-8 -*-

import operator
import capteur

CONFIG = {
    "sqlite-path": "locale.db",

    "ypareo-db": {
        "database": "donneesypareo",
        "user": "ypareo",
        "password": "ypareo",
        "host": "srv-iris-sn",
        "port": 5432,
    },

    "smtp" : {
        "host": "smtp.gmail.com",
        "port": 587,
        "username": "btssnfc@gmail.com",
        "password": "mpdmdqjnspsi",
        "starttls": True,
        "from_addr": "btssnfc@gmail.com",
    },

    "to_addr": "btssnfc@gmail.com",

    "loglevel": 'INFO',
    "logfile": None,

    "capture": False,

    "temporisation": 0.5,

    "i2c-bus": 1,

    "hardware": {
        "buzzer": {
            "label": "Buzzer de fou",
            "action": "write",
            "type": "float",
            "i2c-addr": 4,
            "pin": 9,
        },
        "lumiere": {
            "label": "Eclairage interieur",
            "action": "write",
            "type": "bool",
            "i2c-addr": 4,
            "pin": 10,
        },
        "rfid": {
            "class": capteur.CapteurModBUS,
            "label": "Lecteur carte",
            "action": "read",
            "type": "float",
            "tcp": "192.168.104.200",
            "port": 502,
            "slave": 5,
            "execute": [
               {
                  "operation": operator.eq,
                  "level": 1,
                  "run": "write",
                  "hardware": "lumiere",
                  "value": 1,
               },
               {
                  "operation": operator.eq,
                  "level": 0,
                  "run": "write",
                  "hardware": "lumiere",
                  "value": 0,
               }
            ]
        },
        "capteur": {
            "class": capteur.CapteurI2C,
            "label": "Luminosite",
            "action": "read",
            "type": "float",
            "i2c-addr": 4,
            "pin": 0,
            "execute": [
               {
                  "operation": operator.ge,
                  "level": 150,
                  "run": "write",
                  "hardware": "lumiere",
                  "value": 0,
               },
               {
                  "operation": operator.le,
                  "level": 149,
                  "run": "write",
                  "hardware": "lumiere",
                  "value": 1,
               }
            ]
        },
    },

    "commands": {
        'beep': {
            "i2c-addr": 4,
            "cmd": 2,
        },
        'reset': {
            "i2c-addr": 4,
            "cmd": 1,
        },
    },
}
