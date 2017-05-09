from scripts.device_info import *

for line in deviceList():
    deviceid=str(line)
    print(manufacturer(deviceid))