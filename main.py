from machine import Pin
from time import sleep
import requests
import ubinascii
import jm_bluetooth
import jm_lcd

pin = Pin("LED", Pin.OUT)
# count = 0

# bluetooth
ble_uart = jm_bluetooth.BLEUART()

while not ble_uart.network_connected:
    print("not not connected to wifi")
    sleep(1)

def get_data():
    id = "1007185"
    pw = "ds1007185"
    url = "http://onshore.hanwhaocean.com/auth_test/login"
    bytes = f'{id}:{pw}'.encode('UTF-8')

    credential = ubinascii.b2a_base64(bytes).rstrip().decode('ascii')
    headers = {'Authorization': f'Basic {credential}'}

    res = requests.post(url, headers=headers)
    json = res.json()
    acc_tkn = json['acc_token']

    url = "http://onshore.hanwhaocean.com/auth_test/api/v1/projects"
    headers = {'Authorization': f'Bearer {acc_tkn}'}

    res = requests.get(url, headers=headers)
    data = res.json();
    n_data = len(data['id'])
    # print(len(data['id']))

    for i in range(0, n_data):
        hnum = data['hNumber'][i]
        hname = data['name'][i]

        jm_lcd.print(f"{hnum}:\n{hname}")

        sleep(5)

get_data()

while True:
    try:
        pin.toggle()

        sleep(1) # sec
    except KeyboardInterrupt:
        break

pin.off()
jm_lcd.print("Finishing")
jm_lcd.backlight_off()

print("Finished.")


