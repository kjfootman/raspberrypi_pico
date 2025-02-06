from machine import Pin
from time import sleep
import jm_network
import jm_lcd

SSID = 'SK_WiFiGIGA62FC_2.4G'
PASSWORD = 'JKO50@8518'

pin = Pin("LED", Pin.OUT)
print("LED starts flashing...")

jm_network.connect_to_wlan(SSID, PASSWORD)

count = 0
while True:
    try:
        pin.toggle()
        jm_lcd.print(f'This is a test.\nCount: {count}')

        count += 1
        sleep(2) # sec
    except KeyboardInterrupt:
        break

pin.off()
print("Finished.")

