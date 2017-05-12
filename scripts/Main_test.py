#coding=utf-8

import threading
import time
import configparser

from scripts.create_dirctory import createResultDir
from scripts.device_info import deviceList
from scripts.monkey_test import monkeytest
from scripts.Result_maker import resultMaker
 
config = configparser.ConfigParser()
config.read_file(open('monkeytest.ini'),'r')
runtime=int(config.get('config','Test Time(min)'))
gettime=int(config.get('config','Catch log interval(min)'))
 
createtime=time.strftime('%Y.%m.%d_%H-%M-%S',time.localtime())
createResultDir(createtime)
print(time.ctime()+"~~ :Test result will save in "+createResultDir(createtime)+".")
 
threads = []
 
   
for line in deviceList():
    deviceid=str(line)
  
    t1 = threading.Thread(target=monkeytest,args=(createtime,deviceid,runtime,gettime,))
    threads.append(t1)

resultThread=threading.Thread(target=resultMaker,args=(createResultDir(createtime),))
      
if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
           
    for t in threads:
        t.join()
        
    resultThread.setDaemon(True)
    resultThread.start()
    resultThread.join()