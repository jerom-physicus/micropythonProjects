from machine import UART
from machine import Pin
import time
import machine
import os
import network
import usocket as socket
import gc
import micropython

uart1 = UART(1, baudrate=115200, tx=17, rx=16)
uart1.init(115200, bits=8, parity=None, stop=2)
boot_button_pin = 0
boot_button = Pin(boot_button_pin, Pin.IN, Pin.PULL_UP)
received_code = ''
first_received_line = None
def prints(info):
    uart1.write(info)
    
def sleep(delay):
    time.sleep(delay)# Set up an access point
 
def save_file():
    filename = first_received_line.lstrip("#")
    try:
        os.remove(filename)
    except OSError:
        pass  

    with open(filename, 'w') as f:

        f.write(received_code)
        print("File saved")
        print(first_received_line)

def is_boot_button_pressed():
    # The boot button is usually active LOW, so it will read as 0 when pressed
    return not boot_button.value()

# Main loop to continuously check if the boot button is pressed
time.sleep(2)
apState = 0
time.sleep(1)

if is_boot_button_pressed():
    prints("Boot button is pressed!")
    apState = 1


def run():
    file_name = "index.py"
    try:
        with open(file_name, 'r') as file:
            content = file.read()  # Reads the content of the file
            print("Executing file content:")
            exec(content)
    except Exception as e:
        prints("hello")
        print("Error occurred while reading/execution the file:", e)

if apState:
    prints("reading")
    uart1.write("Writting...")
    while True:
        
        
        try:

            received_line = uart1.readline()
            received_line = received_line.decode()  # Remove .strip() to retain whitespaces
            
            if first_received_line is None:  # Check if this is the first received line
                first_received_line = received_line.strip()  # Save the first line to the variable
            else:
                if received_line.strip() == "END":
                    # Append received code with a newline character and save file
                    save_file()
                    break
                else:
                    received_code += received_line  # Append received line to received_code

        except:
            pass# Catch specific exceptions instead of bare except
            

        time.sleep(0.01)
else:

    run()
    