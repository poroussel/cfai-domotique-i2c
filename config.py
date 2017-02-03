# -*- coding: utf-8 -*-


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
    },

    "loglevel": 'DEBUG',
    
    "frequence": 5,
    
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
            "label": "Potentiomètre",
            "action": "read",
            "type": "float",
            "i2c-addr": 4,
            "pin": 0,
        },
        "presence": {
            "label": "Capteur mouvement",
            "action": "read",
            "type": "float",
            "i2c-addr": 4,
            "pin": 1,
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

