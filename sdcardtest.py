import machine
import os
import sdcard


sd = sdcard.SDCard(machine.SPI( sck=machine.Pin(13), mosi=machine.Pin(14),miso=machine.Pin(12)), machine.Pin(21))


os.mount(sd, "/sd")
print(os.listdir("/sd"))