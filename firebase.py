import network
import urequests
import time
import json
import dht
import machine
import time

# Pin configuration
dht_pin = 15  # Assuming DHT11 sensor is connected to GPIO 4

# Initialize DHT sensor
dht_sensor = dht.DHT11(machine.Pin(dht_pin))

led_pin = 13

# Initialize the LED pin as an output
led = machine.Pin(led_pin, machine.Pin.OUT)

def connect_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    
    if not sta_if.isconnected():
        print("Connecting to WiFi...")
        sta_if.active(True)
        sta_if.connect(ssid, password)
        
        while not sta_if.isconnected():
            pass
        
    print("Connected to WiFi:", sta_if.ifconfig())

def write_to_firebase(key,value):
    # Replace 'YOUR_FIREBASE_PROJECT_ID' and 'YOUR_FIREBASE_DATABASE_KEY' with your actual Firebase project ID and database key
    url = f"https://nova-ad592-default-rtdb.firebaseio.com/data.json?auth=AIzaSyDG4G_mJvAdNgKMnyOHKO2LRuQIWSdGxzI"

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
    url = f"https://nova-ad592-default-rtdb.firebaseio.com/states.json?auth=AIzaSyDG4G_mJvAdNgKMnyOHKO2LRuQIWSdGxzI"

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

    if(vaccum_state == 1):
        led.value(1)
    else:
        led.value(0)
    dht_sensor.measure()  # Perform a measurement
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    
    
    
    data_to_push = {"New data to push to Firebase!"}
    write_to_firebase("esp32", f"{temperature},{humidity}")




    

    

