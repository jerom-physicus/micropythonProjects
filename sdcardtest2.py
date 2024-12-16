import os
from machine import Pin, SoftSPI
from sdcard import SDCard

# Pin assignment:
# MISO -> GPIO 13
# MOSI -> GPIO 12
# SCK  -> GPIO 14
# CS   -> GPIO 27
try:
    os.umount('/sd')  # Unmount the SD card if it was previously mounted
    print("Unmounted previous SD card.")
except OSError:
    pass  # If it's not mounted, we can ignore the error

# Re-initialize the SD card
sd = machine.SDCard(slot=2, sck=13, miso=12, mosi=14, cs=21)
print("sdcard test 1...")
os.mount(sd, "/sd")
print(os.listdir('/sd'))
print("sdcard test end...")
