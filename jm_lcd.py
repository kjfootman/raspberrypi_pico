from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import machine
import time

# I2c 16 * 2 LCD
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

def show_test_string(my_str):
    print("Show test string")
    # set I2C
    i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

    lcd.putstr(my_str)

def print(msg):
    lcd.clear()
    lcd.putstr(msg)

def backlight_off():
    time.sleep(3)
    lcd.clear()
    lcd.backlight_off()