#!/usr/bin/env python
"""
'publish.py'
=========================================
Publishes an incrementing value to a feed

Author(s): Brent Rubell, Todd Treece for Adafruit Industries
"""
# Import standard python modules
import time
import sys

# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed


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


# holds the count for the feed
run_count = 0

aio = Client(ENV_DICT['ADAFRUIT_IO_USERNAME'], ENV_DICT['ADAFRUIT_IO_KEY'])
# Create an instance of the REST client.


while True:
    print('sending count: ', run_count)
    run_count += 1 
    aio.send_data('pi-lcd.message1', run_count)
    aio.send_data('pi-lcd.message2', run_count)
    aio.send_data('pi-lcd.message3', run_count)
    aio.send_data('pi-lcd.message4', run_count)
    aio.send_data('pi-lcd.message5', run_count)
    # Adafruit IO is rate-limited for publishing
    # so we'll need a delay for calls to aio.send_data()
    time.sleep(10)
