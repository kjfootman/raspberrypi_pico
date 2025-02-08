import time
import network
import jm_lcd
from machine import Pin

pin = Pin("LED", Pin.OUT)
pin.off()

def connect_to_wlan(ssid, pwd) -> bool:
    # Connect to WiFi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, pwd)

    max_wait = 10
    count = 0

    while max_wait > 0:
        jm_lcd.print(f"Connecting to\nNetwork. {count}")

        if wlan.status() < 0 | wlan.status() >= 3:
            break

        max_wait -= 1
        count += 1

        print(f'waitting for connection... status: {wlan.isconnected()}')

        if wlan.isconnected():
            break

        time.sleep(1)

    if wlan.status() != 3:
        # raise RuntimeError('network connection failed')
        return False
    else:
        status = wlan.ifconfig()
        print(f'Connected to network. IP address: {status[0]}')

        lcd_str = f'Hello, J.M.\n{status[0]}'
        jm_lcd.print(lcd_str)
        time.sleep(5)

        return True