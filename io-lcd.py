#!/usr/bin/env python3
import time
import sys
import os
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd


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

# Modify this if you have a different sized Character LCD
lcd_columns = 16
lcd_rows = 2

# Initialise I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Initialise the LCD class
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

lcd.clear()

DATA_MESSAGES = []

aio = Client(ENV_DICT['ADAFRUIT_IO_USERNAME'], ENV_DICT['ADAFRUIT_IO_KEY'])


DATA_MESSAGES = {}



while True:
    message1 = aio.receive('pi-lcd.message1')
    message2 = aio.receive('pi-lcd.message2')
    message3 = aio.receive('pi-lcd.message3')
    message4 = aio.receive('pi-lcd.message4')
    message5 = aio.receive('pi-lcd.message5')

    DATA_MESSAGES.update({message1: message1})
    DATA_MESSAGES.update({message2: message2})
    DATA_MESSAGES.update({message3: message3})
    DATA_MESSAGES.update({message4: message4})
    DATA_MESSAGES.update({message5: message5})

    for data in DATA_MESSAGES:
        print(data.value)
        print_message = data.value[:16]+"\n"+data.value[16:]
        lcd.clear()
        lcd.message = print_message
        time.sleep( 5 )


