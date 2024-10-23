from machine import Pin
import time
import machine
boot_button_pin = 0
boot_button = Pin(boot_button_pin, Pin.IN, Pin.PULL_UP)
def init_qbit():
    try:  
        some
    except CustomError as e:
        print(e)
def is_boot_button_pressed():
    # The boot button is usually active LOW, so it will read as 0 when pressed
    return not boot_button.value()

def init_run():
    time.sleep(2)
    apState = 0

    if is_boot_button_pressed():
        print("Boot button is pressed!")
        apState = 1
        
    if apState:
        init_qbit()    

