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

    "collector-url" : "http://127.0.0.1:8000/sensors/api/readings/",

    "to_addr": "btssnfc@gmail.com",

    "loglevel": 'INFO',
    "logfile": None,

    "capture": False,

    "temporisation": 2,

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
        "capteur": {
            "class": capteur.CapteurI2C,
            "label": "Luminosite",
            "action": "read",
            "type": "float",
            "collector-id" : 1,
            "i2c-addr": 4,
            "pin": 0,
            "execute": [
                {
                    "operation": operator.le,
                    "level": 140,
                    "run": "write",
                    "hardware": "lumiere",
                    "value": 1,
                },
                {
                    "operation": operator.le,
                    "level": 140,
                    "run": "beep",
                },
                {
                    "operation": operator.ge,
                    "level": 141,
                    "run": "write",
                    "hardware": "lumiere",
                    "value": 0,
                },
            ],
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
