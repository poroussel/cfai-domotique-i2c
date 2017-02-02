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

    "loglevel": 'DEBUG',
    
    "frequence": 3.5,
    
    "i2c-bus": 1,

    
    "hardware": {
        "buzzer": {
            "label": "Buzzer de fou",
            "action": "write",
            "type": "ms",
            "i2c-addr": 4,
            "pin": 9,
        },
        "capteur": {
            "label": "Capteur chelou",
            "action": "read",
            "type": "float",
            "i2c-addr": 4,
            "pin": 0,
        },
    },

    "commands": {
        'beep': {
            "i2c-addr": 4,
            "cmd": 9,
        },
        'reset': {
            "i2c-addr": 4,
            "cmd": 1,
        },
    },
}

