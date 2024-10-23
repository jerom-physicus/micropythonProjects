import machine
import sdcard
import os

def setup_sd_card():
    # Initialize SPI and SD card
    spi = machine.SoftSPI(baudrate=1000000, polarity=0, phase=0, sck=machine.Pin(13), mosi=machine.Pin(14), miso=machine.Pin(12))
    cs = machine.Pin(21, machine.Pin.OUT)
    
    # Mount SD card
    sd = sdcard.SDCard(spi, cs)
    os.mount(sd, "/sd")
    
    # Move to the SD card as the root file system
    os.chdir('/sd')

    # List files to verify
    print("Files on SD card:")
    print(os.listdir('/sd'))

# Setup SD card as the main file system
setup_sd_card()

# Now the SD card is mounted at /
# You can place your main.py on the SD card root
