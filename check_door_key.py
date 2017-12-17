import requests
from bluepy import btle
from bluepy.btle import BTLEException
from time import sleep
import sys

ESP_MAC_ADDR = "BLE_MAC_ADDRESS"
CONNECTION_RETRY = 5

def s8(value):
    return -(value & 0b10000000) | (value & 0b01111111)

def judge_thresh_x(x):
    if x < 7:
        return True
    else:
        return False

def judge_thresh_y(y):
    if y > -10:
        return True
    else:
        return False

def judge(x, y):
    if judge_thresh_x(x) == True and judge_thresh_y(y) == True:
        return True

def connect_with_retry():
    for i in range(1, CONNECTION_RETRY+1):
        try:
            tPeripheral = btle.Peripheral(deviceAddr=ESP_MAC_ADDR)
        except BTLEException as e:
            print('error:{e} retry:{i}/{max}'.format(e=e, i=i, max=CONNECTION_RETRY))
            sleep(3)
        else:
            return tPeripheral
    print('critical')
    sys.exit()

#main
tPeripheral = connect_with_retry()
tCharList = tPeripheral.getCharacteristics()

tChar = next(tChar for tChar in tCharList if tChar.getHandle() == 0x002a)

raw_data = tChar.read()
x = s8(raw_data[0])
y = s8(raw_data[1])
z = s8(raw_data[2])

print('X=' + str(x) + ' Y=' + str(y) + ' Z=' + str(z))

if judge(x, y)==True:
    print('Door key is opened!!')
    requests.post('https://maker.ifttt.com/trigger/door_key_opened/with/key/MZX8aaqwNrtki4NynulzE')
