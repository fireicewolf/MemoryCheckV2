#coding=utf-8

import threading
import time
import configparser

from scripts.create_dirctory import createResultDir
from scripts.device_info import deviceList
from scripts.monkey_test import getAppPackageName
from scripts.monkey_test import monkeytest
from scripts.Result_maker import resultMaker
 
config = configparser.ConfigParser()
config.read_file(open('monkeytest.ini'), 'r')
runtime = int(config.get('config', 'Test Time(min)'))
gettime = int(config.get('config', 'Catch log interval(min)'))
 
createtime = time.strftime('%Y.%m.%d_%H-%M-%S', time.localtime())
createResultDir(createtime)
print(time.ctime()+"~~ :Test result will save in "+createResultDir(createtime)+".")
 
threads = []

for line in deviceList():
    deviceid = str(line)
    testpackages = (config.get('config', 'Test Packages'))
    
    if testpackages == '':
        testpackagenames = getAppPackageName(createtime, deviceid)
    else:
        testpackages = testpackages.split(',')
        testpackagenames = ''
        for line in testpackages:
            testpackagenames += '-p '+line+' '
        print(time.ctime()+"~~ Device "+deviceid+':Packages '+str(testpackages)+' will be tested.')
  
    t1 = threading.Thread(target=monkeytest, args=(createtime, deviceid, testpackagenames, runtime, gettime,))
    threads.append(t1)
 
resultThread=threading.Thread(target=resultMaker, args=(createResultDir(createtime),))
       
if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
            
    for t in threads:
        t.join()
         
    resultThread.setDaemon(True)
    resultThread.start()
    resultThread.join()
