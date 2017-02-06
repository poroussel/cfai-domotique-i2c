# -*- coding: utf-8 -*-

import operator

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
        "host": "",
        "port": 0,
        "username": "",
        "password": "",
        "starttls": False,
        "from_addr": "toto@titi.com",
    },

    "loglevel": 'INFO',
    "logfile": None,
    
    "temporisation": 1,
    
    "i2c-bus": 1,
    
    "hardware": {
        "buzzer": {
            "label": "Buzzer de fou",
            "action": "write",
            "type": "ms",
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
            "label": "Luminosité",
            "action": "read",
            "type": "float",
            "i2c-addr": 4,
            "pin": 0,
            "execute": [
                {
                    "operation": operator.ge,
                    "level": 150,
                    "run": "capture",
                }
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

