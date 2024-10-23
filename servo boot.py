import machine
from time import sleep

# Define the GPIO pin for the servo motor and the boot button
servo_pin = machine.Pin(47)
boot_button = machine.Pin(0, machine.Pin.IN)  # GPIO 0 is usually the boot button

# Set up PWM for the servo (50 Hz for most servos)
pwm = machine.PWM(servo_pin, freq=50)

# Variable to keep track of the servo state
current_angle = 0

# Function to set the angle of the servo
def set_servo_angle(angle):
    # Convert the angle (0-180 degrees) to a duty cycle (between 40 and 115)
    duty = int((angle / 180.0) * 75 + 40)
    pwm.duty(duty)

# Set the initial angle to 0
set_servo_angle(50)
condition = 0
# Main loop to check for boot button presses
while True:
    #print(boot_button.value())
    if(boot_button.value() == 0):
        if(condition == 0):
            condition = 1
            set_servo_angle(50)
        else:
            condition = 0
            set_servo_angle(100)
        
    print(condition)
    
    
        
    sleep(0.2)  # Small delay to avoid unnecessary CPU usage
