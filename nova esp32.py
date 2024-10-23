import network
import urequests
import time
import json
import dht
import machine
import time
from time import sleep


# Define UART parameters
TX_PIN = 14  # GPIO pin for TX
RX_PIN = 16  # GPIO pin for RX
BAUD_RATE = 9600


# Pin configuration
dht_pin = 15  # Assuming DHT11 sensor is connected to GPIO 4

# Initialize DHT sensor
dht_sensor = dht.DHT11(machine.Pin(dht_pin))
uart = machine.UART(1, baudrate=BAUD_RATE, tx=TX_PIN, rx=RX_PIN)

buzzer_pin = 4
vaccum_pin = 13
uv_pin = 12
auto_pin = 14
indicator_pin = 2

vaccum = machine.Pin(vaccum_pin, machine.Pin.OUT)
uv = machine.Pin(uv_pin, machine.Pin.OUT)
auto = machine.Pin(auto_pin, machine.Pin.OUT)

indiactor = machine.Pin(indicator_pin, machine.Pin.OUT)

temperature = 0
humidity = 0
auto.value(0)
uplodecount = 0
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
def connecting():
    CONNECTED_MELODY = [
    (3000, 500),  # Note 1
    
   
]
    for note in CONNECTED_MELODY:
        pwm = machine.PWM(machine.Pin(buzzer_pin), freq=note[0])
        time.sleep_ms(note[1])
        pwm.deinit()

def state():
    CONNECTED_MELODY = [
    (4000, 200),  # Note 1
    
   
]
    for note in CONNECTED_MELODY:
        pwm = machine.PWM(machine.Pin(buzzer_pin), freq=note[0])
        time.sleep_ms(note[1])
        pwm.deinit()
def read_dht_sensor():
    try:
        dht_sensor.measure()  # Perform a measurement
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temperature, humidity
    except Exception as e:
        print("Error reading DHT sensor:", e)
        return 0, 0
# Initialize the LED pin as an output


def connect_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    
    if not sta_if.isconnected():
        print("Connecting to WiFi...")
        connecting()
        sta_if.active(True)
        sta_if.connect(ssid, password)
        
        while not sta_if.isconnected():
            pass
        
    print("Connected to WiFi:", sta_if.ifconfig())
    indiactor.value(1)
    connected()

def write_to_firebase(key,value):
    # Replace 'YOUR_FIREBASE_PROJECT_ID' and 'YOUR_FIREBASE_DATABASE_KEY' with your actual Firebase project ID and database key
    url = f"https://nova-app-39572-default-rtdb.firebaseio.com/data.json?auth=AIzaSyBUehR2gN_XrOG4-OeDTlVtCxECeI0K0Ho"

    payload = {key: value}
    headers = {"Content-Type": "application/json"}

    response = urequests.put(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("ok")
        
    else:
        print("Error setting data:", response.text)
    print("Push Response:", response.text)
    response.close()

def read_from_firebase(data):
    # Replace 'YOUR_FIREBASE_PROJECT_ID' and 'YOUR_FIREBASE_DATABASE_KEY' with your actual Firebase project ID and database key
    url = f"https://nova-app-39572-default-rtdb.firebaseio.com/states.json?auth=AIzaSyBUehR2gN_XrOG4-OeDTlVtCxECeI0K0Ho"
    response = urequests.get(url)

    if response.status_code == 200:
        data = response.json()
        #print("Data retrieved:", str(data))
    else:
        print("Error getting data:", response.text)
    return data


# WiFi credentials
wifi_ssid = "T E S L A 4g"
wifi_password = "87654321"

# Connect to WiFi
connect_wifi(wifi_ssid, wifi_password)

# Write data to Firebase

uv_state = 0
def uplodedata():
    temperature, humidity = read_dht_sensor()
    if temperature is not None and humidity is not None:    
            #print("Temperature: {:.2f}°C, Humidity: {:.2f}%".format(temperature, humidity))
        write_to_firebase("esp32", f"{temperature},{humidity}")
        print("sent")
uplodedata()
while True:
    data = str(read_from_firebase("j"))
    # Given string
    #data = "{'esp32': '29,79,1,0'}"
    key, value = data.strip("{}").split(':')

# Extracting the values string and splitting by comma
    values = value.strip().strip("'").split(',')

# Converting values to integers
    result_list = [int(val) for val in values]

    vaccum_state = result_list[0]
    uv_state = result_list[1]
    auto_state = result_list[2]


    if(vaccum_state == 1):
        vaccum.value(1)

        
        state()
    else:
        vaccum.value(0)
        #print("led is offf")
        
    if(uv_state == 1):
        uv.value(1)
        print("led is on")
        state()
    else:
        uv.value(0)
        
    if(auto_state == 1):
        #uart.write("auto")
        auto.value(1)
        state()
        
    else:
        auto.value(0)
     
    
    if (uplodecount == 20 or uplodecount == 0):
        uplodedata()
        uplodecount = 0
    uplodecount = uplodecount+1
        


