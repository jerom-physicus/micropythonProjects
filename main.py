import machine
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep
import network
import time

from time import sleep
I2C_ADDR = 0x27
totalRows = 4
totalColumns = 20
buzzer_pin = 15 
i2c = SoftI2C(scl=Pin(22), sda=Pin(23), freq=1000000)  # Initializing the I2C method for ESP32
# i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)       # Initializing the I2C method for ESP8266

lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)
lcd.blink_cursor_on()
def connected():
    CONNECTED_MELODY = [
    (3000, 150),  # Note 1
    (3500, 150),  # Note 2
    (4000, 150),  # Note 3
    (5500, 150),  # Note 4 (longer duration)
]
    for note in CONNECTED_MELODY:
        pwm = machine.PWM(machine.Pin(buzzer_pin), freq=note[0])
        time.sleep_ms(note[1])
        pwm.deinit()

def start():
    CONNECTED_MELODY = [
    (5500, 200),  # Note 1
    (3500, 150),  # Note 2
    (2500, 200),  # Note 3
    (5500, 250),  # Note 4 (longer duration)
]
    for note in CONNECTED_MELODY:
        pwm = machine.PWM(machine.Pin(buzzer_pin), freq=note[0])
        time.sleep_ms(note[1])
        pwm.deinit()

def error():
    CONNECTED_MELODY = [
    (3000, 150),  # Note 1
    (2200, 100),  # Note 2  # Note 3
    (500, 300),  # Note 4 (longer duration)
]
    for note in CONNECTED_MELODY:
        pwm = machine.PWM(machine.Pin(buzzer_pin), freq=note[0])
        time.sleep_ms(note[1])
        pwm.deinit()
def enter():
    CONNECTED_MELODY = [
    (2500, 150)  # Note 2
    # Note 4 (longer duration)
]
    for note in CONNECTED_MELODY:
        pwm = machine.PWM(machine.Pin(buzzer_pin), freq=note[0])
        time.sleep_ms(note[1])
        pwm.deinit()

def ls_dir():
    global code
    file_list = os.listdir()
    for file in file_list:        
        code+="#"+file+'\n'
    lcd_display(code)
    
def clear():
    global code
    code=''''''
    lcd.clear()
    start()
def wifi(i,p):
    global code
    net = network.WLAN(network.STA_IF)
    net.active(True)

    while True:
        try:
            net.connect(i,p)
        except OSError as e:
            print(e)
        sleep(1)
        if net.isconnected():
            print('Connected')
            code+="#"+"connected..."+'\n'
            lcd_display(code)
            connected()
            

        break
def wifi_mode():
    net.isconnected()
def lcd_display(code):
    lcd.clear()
    lines = code.strip().split('\n')
    modified_lines = []

    for line in lines:
        if len(line) > 20:
            modified_lines.append(line[:20])
            modified_lines.append(line[20:])
        else:
            modified_lines.append(line)

    modified_code = '\n'.join(modified_lines)
    last_4_lines = modified_code.strip().split('\n')[-4:]
    row = 0
    for line in last_4_lines:
        print(line)
        lcd.move_to(0, row)
        lcd.putstr(line)
        row+=1

def cal(x):
    global code
    result = eval(str(x))
    code+="#"+str(result)+'\n'
    lcd_display(code)
    return result

def log(x):
    global code
    code+="#"+str(x)+'\n'
    lcd_display(code)
code = '''
'''  
while True:
    y = input("Enter: ")
    if y != "/e":        
        code+=y+'\n'
        lcd_display(code)
        enter()
    else:
        print(code)
        try:
            exec(code, globals(), locals())
        except Exception as e: 
            code+="#"+str(e)+'\n'
            lcd_display(code)
            print(code)
        
#new commit is added to my repo