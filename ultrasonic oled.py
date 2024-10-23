from machine import Pin, I2C
from time import sleep_ms
from sh1106 import SH1106_I2C

# Import ultrasonic sensor related libraries
from machine import time_pulse_us

# Initialize I2C and OLED display
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
oled = SH1106_I2C(128, 64, i2c, None, addr=0x3C)
oled.sleep(False)

# Initialize ultrasonic sensor pins
TRIGGER_PIN = 18
ECHO_PIN = 19
trigger = Pin(TRIGGER_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

def get_distance():
    # Send a 10us pulse to trigger pin
    trigger.value(1)
    sleep_ms(1)
    trigger.value(0)
    # Measure the duration of the echo pulse
    duration = time_pulse_us(echo, 1, 30000)  # Maximum distance: 500cm
    # Calculate distance from duration
    distance = duration * 0.0343 / 2  # Speed of sound = 343 m/s
    return distance

while True:
    distance = get_distance()  # Measure distance
    oled.fill(0)
    oled.text('Qbit Tech', 25, 2)
    oled.text('Distance:', 0, 25)
    oled.text('{:.2f} cm'.format(distance), 0, 40)  # Display distance
    oled.show()
    sleep_ms(100)

