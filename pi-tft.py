#!/usr/bin/env python3
import sys,os,time,subprocess
import curses, requests, json
from Adafruit_IO import Client, Group
import search

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

    
def fetch_json_data():
    JSON_DATA_MESSAGES = {}
    qualys = requests.get('https://status.qualys.com/api/v2/status.json')
    qualys_json = qualys.json()
    message1 = "|| Qualys-status || indicator: %s | description %s" %(qualys_json['status']['indicator'], qualys_json['status']['description'] )
    JSON_DATA_MESSAGES.update({message1: message1})
    return JSON_DATA_MESSAGES

def fetch_splunk_data():
    thing = search.__main__("search sourcetype=ifttt earliest=-24h latest=now| sort 1 -_time| table tag motion")
    print(thing)
    return thing

def fetch_data():
    DATA_MESSAGES = {}
    aio = Client(ENV_DICT['ADAFRUIT_IO_USERNAME'], ENV_DICT['ADAFRUIT_IO_KEY'])
     
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

 
    return DATA_MESSAGES

def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    timecounter=0
    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        # Declaration of strings
        title = "Curses example"[:width-1]
        subtitle = "Written by Clay McLeod"[:width-1]
        keystr = "Last key pressed: {}".format(k)[:width-1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
        if k == 0:
            keystr = "No key press detected..."[:width-1]

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        #ignoring the centering
        a=1
        start_y=a
        # Rendering some text
        #whstr = "Width: {}, Height: {}".format(width, height)
        #stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        #stdscr.attron(curses.color_pair(2))
        #stdscr.attron(curses.A_BOLD)

        # Rendering title
        #stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        #stdscr.attroff(curses.color_pair(2))
        #stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        #stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        #stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        #stdscr.addstr(start_y + 5, start_x_keystr, keystr)

        if (timecounter == 0) or (timecounter > 60):
            DATA=fetch_data()
            DATA_JSON=fetch_json_data()
            timecounter+=1
        
        for i in DATA:
            stdscr.addstr(start_y + int(a), 0, str(DATA[i].value))
            a=a+1
        
        for i in DATA_JSON:
            stdscr.addstr(start_y + int(a), 0, str(DATA_JSON[i]))
            a=a+1

        stdscr.addstr(start_y + int(a), 0, str(fetch_splunk_data()))
  



        stdscr.move(cursor_y, cursor_x)
        # Refresh the screen
        stdscr.refresh()
        time.sleep(1)

        # Wait for next input
        k = stdscr.getch()

def main():

    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()