import threading
import queue
import time
from getkey import getkey

def onKeyInput():
    global onoff_flag
    
    while (True):
        key = getkey()
        if key == 't':
            if onoff_flag:
                onoff_flag = False
            else:
                onoff_flag = True

def main():
    global onoff_flag
    
    onoff_flag = False

    keyThread = threading.Thread(target=onKeyInput)
    keyThread.daemon = True 
    keyThread.start()

    while (True):
        print(onoff_flag)

        time.sleep(0.5)

if __name__ == "__main__" :
    main()