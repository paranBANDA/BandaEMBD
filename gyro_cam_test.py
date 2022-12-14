import smbus			#import SMBus module of I2C
from time import sleep          #import
import picamera
import time
import requests
import info
import json

PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

idx = 0
tAx = 0
tAy = 0
tAz = 0 
tGx = 0
tGy = 0
tGz = 0

def MPU_Init():
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	bus.write_byte_data(Device_Address, CONFIG, 0)	
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)	
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    value = ((high << 8) | low)        
    if(value > 32768):
            value = value - 65536
    return value

def capture_img():
    camera.capture('snapshot'+str(idx)+'.jpg')
    send_img()
    idx += 1

def send_img():
    f = open('snapshot'+str(idx)+'.jpg', 'rb')
    requests.post('http://13.124.202.212:3000/polaroid/uploaddiaryimage', files={'files':f}, data=json.dumps(info.info))
    f.close()

bus = smbus.SMBus(0) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

camera = picamera.PiCamera()
camera.resolution = (2592, 1944) # (64, 64) ~ (2592, 1944) px

while True:
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)

    Ax = acc_x/16384.0
    Ay = acc_y/16384.0
    Az = acc_z/16384.0	
    Gx = gyro_x/131.0
    Gy = gyro_y/131.0
    Gz = gyro_z/131.0

    gyro = 0
    if gyro == 1:
        capture_img()

    sleep(5)