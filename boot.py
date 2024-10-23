from machine import Pin
import time
import machine
import os
boot_button_pin = 0
boot_button = Pin(boot_button_pin, Pin.IN, Pin.PULL_UP)

print("Welcome to Qbit Micropython (^_^)")
def init_qbit():
    try:  
        some
    except BootEnable as e:
        print(e)
def is_boot_button_pressed():
    # The boot button is usually active LOW, so it will read as 0 when pressed
    return not boot_button.value()

def init_run():
    time.sleep(1)
    apState = 0

    if is_boot_button_pressed():
        list = os.listdir()
        print("------------------")
        for i in range(len(list)):
            
            print(list[i])
        print("------------------") 
        print("Ready to upload")
        apState = 1
        
    if apState:
        init_qbit()    
init_run()
def save(filename,code):
    try:
        os.remove(filename)
    except OSError:
        pass  
    with open(filename, 'w') as f:
        f.write(code)
        print("File saved sucessfully...")
#save