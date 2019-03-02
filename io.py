#!/usr/bin/env python3
import time
import sys
import os
# Import Adafruit IO MQTT client.

from Adafruit_IO import Client, Group

ENV_DICT = {}
ENV_VARS = [
    "ADAFRUIT_IO_KEY",
    "ADAFRUIT_IO_USERNAME"
    ]

for var in ENV_VARS:
    if os.getenv(var) is None:
        print(("Environment variable %s not set it is required")% var)
        sys.exit(1)
    ENV_DICT.update({var: os.getenv(var)})

DATA_MESSAGES = []

aio = Client(ENV_DICT['ADAFRUIT_IO_USERNAME'], ENV_DICT['ADAFRUIT_IO_KEY'])


DATA_MESSAGES = {}



while True:
    time.sleep( 5 )
    message1 = aio.receive('pi-lcd.message1')
    message2 = aio.receive('pi-lcd.message2')

    DATA_MESSAGES.update({message1: message1})
    DATA_MESSAGES.update({message2: message2})

    for data in DATA_MESSAGES:
        print(data.value)


