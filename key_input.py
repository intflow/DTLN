import threading
import queue
import time
from getkey import getkey, keys
import sys

def onKeyInput():
    global onoff_flag, end_flag
    
    while (True):
        key = getkey()
        if key == 't':
            if onoff_flag:
                onoff_flag = False
                print("[OFF]AudioProcess")
            else:
                onoff_flag = True
                print("[ON]AudioProcess")
        if key == keys.ENTER:
            end_flag = True
            print("----Terminate Program----")
            sys.exit()
            break
            

def main():
    global onoff_flag, end_flag
    
    onoff_flag = False
    end_flag = False

    keyThread = threading.Thread(target=onKeyInput)
    keyThread.daemon = True 
    keyThread.start()

    while (True):
        print(onoff_flag)
        
        if end_flag:
            break

        time.sleep(0.5)
        
    print("End")

if __name__ == "__main__" :
    main()