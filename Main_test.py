#coding=utf-8

import configparser
import threading
import time

from scripts.Result_maker_new import resultMakerNew
from scripts.create_dirctory import createResultDir
from scripts.device_info import deviceList
from scripts.monkey_test import getAppPackageName
from scripts.monkey_test import randomMonkeyTest
from scripts.monkey_test import sequenceMonkeyTest

config = configparser.ConfigParser()
config.read_file(open('monkey_test_config.ini'), 'r')
running_time = int(config.get('config', 'Test Time(min)'))
catch_log_interval = int(config.get('config', 'Catch log interval(min)'))
random_package_test = str(config.get('config', 'Random package test'))
event_interval = int(config.get('config', 'Event interval'))
event_count = int(config.get('config', 'Event count'))
def_test_package = str(config.get('config', 'Test Packages'))
is_screen_off = str(config.get('config', 'Screen off'))
screen_off_time = '%.2f' % float(config.get('config', 'Screen off time'))
 
create_dir_time = time.strftime('%Y.%m.%d_%H-%M-%S', time.localtime())
print(time.ctime() + "~~ : Test result will save in " + createResultDir(create_dir_time) + ".")
 
threads = []


for device in deviceList():
    device_id = str(device)
    
    if def_test_package == '':
        packages = getAppPackageName(create_dir_time, device_id)
        if random_package_test == 'yes':
            test_package_names = ''
            for line in packages:
                if line == '\n':
                    pass
                else:
                    line = line.strip('\n')
                    test_package_names += '-p '+line+' '
        else:
            test_package_names = packages
    else:
        packages = def_test_package.strip(' ')
        packages = packages.split(',')
        if random_package_test == 'yes':
            test_package_names = ""
            for package in packages:
                test_package_names += '-p ' + package + ' '
            print(time.ctime() + "~~ Device " + device_id + ':Packages ' + str(packages) + ' will be tested.')
        else:
            test_package_names = packages

    if random_package_test == 'yes':
        t1 = threading.Thread(target=randomMonkeyTest, args=(create_dir_time, device_id, test_package_names,
                                                             event_interval, event_count, running_time,
                                                             catch_log_interval, is_screen_off, screen_off_time))
        threads.append(t1)
    else:
        t1 = threading.Thread(target=sequenceMonkeyTest, args=(create_dir_time, device_id, test_package_names,
                                                               running_time, event_interval, event_count, is_screen_off,
                                                               screen_off_time))
        threads.append(t1)

resultThread = threading.Thread(target=resultMakerNew, args=(createResultDir(create_dir_time),))

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

    resultThread.setDaemon(True)
    resultThread.start()
    resultThread.join()
    print(time.ctime() + ': Test finished.')
