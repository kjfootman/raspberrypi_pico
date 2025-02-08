from machine import Pin
from time import sleep
import jm_network
import jm_lcd
import requests
# import base64
import ubinascii

SSID = 'SK_WiFiGIGA62FC_2.4G'
PASSWORD = 'JKO50@8518'

pin = Pin("LED", Pin.OUT)
count = 0
# print("LED starts flashing...")

# connect to network
is_conn = jm_network.connect_to_wlan(SSID, PASSWORD)

if not is_conn:
    # if failed to connect to network.
    jm_lcd.print('Network Conn.\nFailed.')
    sleep(3)

def get_data():
    id = "1007185"
    pw = "ds1007185"
    url = "http://onshore.hanwhaocean.com/auth_test/login"
    bytes = f'{id}:{pw}'.encode('UTF-8')

    credential = ubinascii.b2a_base64(bytes).rstrip().decode('ascii')
    # print(f"credential: {credential}")
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
        # info = f"{hnum}:\n{hname}"
        jm_lcd.print(f"{hnum}:\n{hname}")
        sleep(5)


get_data()

while True & is_conn:
    try:
        pin.toggle()
        jm_lcd.print(f'This is a test.\nCount: {count}')


        count += 1
        sleep(1) # sec
    except KeyboardInterrupt:
        break

pin.off()
jm_lcd.print("Finishing")
jm_lcd.backlight_off()

print("Finished.")


