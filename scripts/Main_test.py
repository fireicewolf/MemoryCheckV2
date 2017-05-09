#coding=utf-8

import threading
import time
import configparser

from scripts.create_dirctory import createResultDir
from scripts.device_info import deviceList
from scripts.monkey_test import monkeytest

createtime=time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime())
createResultDir(createtime)

config = configparser.ConfigParser()
config.read_file(open('monkeytest.ini'),'r')
runtime=int(config.get('config','Test Time(min)'))
gettime=int(config.get('config','Catch log interval(min)'))

threads = []
 
for line in deviceList():
    deviceid=str(line)

    t1 = threading.Thread(target=monkeytest,args=(createtime,deviceid,runtime,gettime,))
    threads.append(t1)
    
if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
         
    for t in threads:
        t.join()