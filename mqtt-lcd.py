#!/usr/bin/env python3
import time
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import sys
import os
# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

ENV_VARS = [
    "ADAFRUIT_IO_KEY",
    "ADAFRUIT_IO_USERNAME"
    ]

for var in ENV_VARS:
    if os.getenv(var) is None:
        print(("Environment variable %s not set it is required")% var)
        sys.exit(1)
    ENV_DICT.update({var: os.getenv(var)})

# Modify this if you have a different sized Character LCD
lcd_columns = 16
lcd_rows = 2

# Initialise I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Initialise the LCD class
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

lcd.clear()
# Set LCD color to purple
lcd.color = [50, 0, 50]


# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = ENV_DICT['ADAFRUIT_IO_KEY']

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = ENV_DICT['ADAFRUIT_IO_USERNAME']

# Set to the ID of the feed to subscribe to for updates.
# Group Name
group_name = 'pi-lcd'

# Feeds within the group
group_feed_one = 'message1'
group_feed_two = 'message2'



# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to topic changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Listening for changes on ', group_name)
    # Subscribe to changes on a group, `group_name`
    client.subscribe_group(group_name)

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    lcd.message = payload


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

# Start a message loop that blocks forever waiting for MQTT messages to be
# received.  Note there are other options for running the event loop like doing
# so in a background thread--see the mqtt_client.py example to learn more.
client.loop_background()