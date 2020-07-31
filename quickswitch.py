import time
import pynput
import math
import threading

lock = False

def unlock():
    global lock
    lock = False

def getTime():
    return time.time()*1000

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))

def quickSwitch():
    global lock
    with keyboard.pressed(pynput.keyboard.Key.alt):
        if not lock:
            keyboard.press(pynput.keyboard.Key.tab)
            keyboard.release(pynput.keyboard.Key.tab)
            threading.Timer(LOCK_DURATION, unlock)

def on_move(x, y):
    global ppos, ptime
    cpos = (x, y)
    ctime = getTime()
    if  ctime >=  (ptime + SAMPLERATE):
        if  distance(cpos, ppos) > THRESHOLD:
            quickSwitch()
        ppos = cpos
        ptime = ctime



def on_click(x, y, button, pressed):
    if button == pynput.mouse.Button.middle and not pressed:
        return False

#CONSTANTS
THRESHOLD = 400 #pixels
SAMPLERATE = 10 #ms
LOCK_DURATION  = 0.5 #s

keyboard = pynput.keyboard.Controller()
mouse = pynput.mouse.Controller()
ppos = mouse.position
ptime = getTime()

with pynput.mouse.Listener(on_move=on_move, on_click=on_click) as listener:
    print("quickswitcher now listening press MOUSE_BUTTON_3 to exit")
    listener.join()


