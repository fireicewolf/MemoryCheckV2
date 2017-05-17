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
config.read_file(open('monkey_test_config.ini'), 'r')
test_running_time = int(config.get('config', 'Test Time(min)'))
catch_log_interval = int(config.get('config', 'Catch log interval(min)'))
 
create_dir_time = time.strftime('%Y.%m.%d_%H-%M-%S', time.localtime())
createResultDir(create_dir_time)
print(time.ctime() + "~~ :Test result will save in " + createResultDir(create_dir_time) + ".")
 
threads = []

for device in deviceList():
    device_id = str(device)
    test_package = (config.get('config', 'Test Packages'))
    
    if test_package == '':
        test_package_names = getAppPackageName(create_dir_time, device_id)
    else:
        test_package = test_package.split(',')
        test_package_names = ''
        for package in test_package:
            test_package_names += '-p ' + package + ' '
        print(time.ctime() + "~~ Device " + device_id + ':Packages ' + str(test_package) + ' will be tested.')
  
    t1 = threading.Thread(target=monkeytest, args=(create_dir_time, device_id, test_package_names, test_running_time, catch_log_interval,))
    threads.append(t1)
 
resultThread=threading.Thread(target=resultMaker, args=(createResultDir(create_dir_time),))
       
if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
            
    for t in threads:
        t.join()
         
    resultThread.setDaemon(True)
    resultThread.start()
    resultThread.join()
