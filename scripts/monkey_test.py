#coding=utf-8
import os
import time

from .command_line import commandLine

from .create_dirctory import createpackageListDir

from .device_info import adbstate

from .save_files import saveAdbLog
from .save_files import saveMemInfoBeforeTest
from .save_files import saveMemInfo
from .save_files import saveMemInfoAfterClearProcess


def getAppPackageName(create_time,device_id):
    installViewApk_cmd = 'adb -s '+device_id+' install -r -g package_name_viewer.apk'
    commandLine(installViewApk_cmd).wait(10)
    
    launchViewApk_cmd = 'adb -s '+device_id+' shell am start -n com.gionee.packages/com.gionee.packages.MainActivity'
    commandLine(launchViewApk_cmd).wait(10)

    saveListToPC_cmd = 'adb -s '+device_id+' pull /sdcard/packages_visual.txt ' + \
                       createpackageListDir(create_time, device_id)+'packages_names_list.txt'
    commandLine(saveListToPC_cmd).wait(10)
    
    uninstallViewApk_cmd = 'adb -s '+device_id+' uninstall com.gionee.packages'
    commandLine(uninstallViewApk_cmd).wait(10)
    
    removeListInPhone_cmd = 'adb -s '+device_id+' shell rm /sdcard/packages_visual.txt'
    commandLine(removeListInPhone_cmd).wait(10)

    print(time.ctime()+"~~ Device "+device_id+":Get app's package names success.")
    
    openapplists = open(createpackageListDir(create_time, device_id)+'packages_names_list.txt', 'r')
    applists = openapplists.readlines()
    openapplists.close()
    
    print(time.ctime()+"~~ Device "+device_id+':App lists load successfully, total '+str(len(applists))+' apps.')
    
    test_packages = ''
    
    for line in applists:
        line = line.strip('\n')
        test_packages += '-p '+line+' '
    return test_packages


def killMonkeyTestProcess(device_id):
    viewMonkeyTestProcess_cmd = 'adb -s '+device_id+' shell "ps | grep monkey"'
    MonkeyTestProcess = commandLine(viewMonkeyTestProcess_cmd).stdout.read()
    MonkeyTestProcess = MonkeyTestProcess.decode()
    MonkeyTestProcess = MonkeyTestProcess.split(' ')[5]
    
    killMonkeyTestProcess_cmd = 'adb -s '+device_id+' shell kill '+str(MonkeyTestProcess)
    commandLine(killMonkeyTestProcess_cmd).wait(10)


#Definition for result save
def monkeytest(create_time, device_id, test_package_names, running_time, catch_log_interval):
    print(time.ctime()+"~~ Device "+device_id+':Rebooting, please wait.')
    deviceReboot_cmd='adb -s '+device_id+' reboot'
    commandLine(deviceReboot_cmd).wait(10)
    adbWaitForDevice_cmd='adb -s '+device_id+' wait-for-device'
    commandLine(adbWaitForDevice_cmd).wait(60)

    print(time.ctime()+"~~ Device "+device_id+':Wait 30s for device stable.')
    time.sleep(30)
    
    count = int(running_time*60*60*1000/500)
    
    if adbstate(device_id) == "device":
        print(time.ctime()+"~~ Device "+device_id+':Adb connection successful, wait for 5 minutes before test')
        time.sleep(300)
        
        print(time.ctime()+"~~ Device "+device_id+':Catching memory info before test.')
        saveMemoryInfoBeforeTest = 'adb -s '+device_id+' shell dumpsys meminfo > ' + \
                                 saveMemInfoBeforeTest(create_time, device_id)
        commandLine(saveMemoryInfoBeforeTest).wait(30)
    
        print(time.ctime()+"~~ Device "+device_id+':Starting monkey test.')
        monkey_cmd = 'adb -s '+device_id+' shell monkey '+test_package_names + \
                     '--throttle 500 --ignore-crashes --ignore-security-exceptions ' \
                     '--ignore-timeouts --monitor-native-crashes -v -v ' + \
                     str(count)+' > '+saveAdbLog(create_time, device_id)
        commandLine(monkey_cmd)
    
        running_count = int(running_time/catch_log_interval)
        
        for i in range(running_count-1):
    
            time.sleep(catch_log_interval*60)
            
            print(time.ctime()+"~~ Device "+device_id+':Catching memory info.')
            saveMemoryInfo_cmd = 'adb -s '+device_id+' shell dumpsys meminfo > '+saveMemInfo(create_time, device_id)
            commandLine(saveMemoryInfo_cmd).wait(30)
            try:
                print(time.ctime()+"~~ Device "+device_id+':Killing monkey test process.')
                killMonkeyTestProcess(device_id)
                print(time.ctime()+"~~ Device "+device_id+':Monkey test process killed.')
            
            except:
                print(time.ctime()+"~~ Device "+device_id+":Did not found monkey test process.")
                
            print(time.ctime()+"~~ Device "+device_id+':Killing background processes.')
            killAllBackgroundApps_cmd = 'adb -s '+device_id+' shell am kill-all'
            commandLine(killAllBackgroundApps_cmd).wait(30)
            
            print(time.ctime()+"~~ Device "+device_id+':Catching memory info after clear processes.')
            saveMemoryInfoAfterClearProcess_cmd = 'adb -s '+device_id+' shell dumpsys meminfo > '+\
                                                  saveMemInfoAfterClearProcess(create_time, device_id)
            commandLine(saveMemoryInfoAfterClearProcess_cmd).wait(30)
    
            print(time.ctime()+"~~ Device "+device_id+':Starting monkey test.')
            monkey_cmd = 'adb -s '+device_id+' shell monkey '+test_package_names + \
                         '--throttle 500 --ignore-crashes --ignore-security-exceptions ' \
                         '--ignore-timeouts --monitor-native-crashes -v -v '\
                         + str(count)+' > '+saveAdbLog(create_time, device_id)
            commandLine(monkey_cmd)
        
        time.sleep(catch_log_interval*60)
        
        print(time.ctime()+"~~ Device "+device_id+':Catching memory info.')
        saveMemoryInfo_cmd = 'adb -s '+device_id+' shell dumpsys meminfo > '+saveMemInfo(create_time, device_id)
        commandLine(saveMemoryInfo_cmd).wait(30)
        
        try:
            print(time.ctime()+"~~ Device "+device_id+':Killing monkey test process.')
            killMonkeyTestProcess(device_id).wait(30)
            print(time.ctime()+"~~ Device "+device_id+':Monkey test process killed.')
        
        except:
            print(time.ctime()+"~~ Device "+device_id+":Did not found monkey test process.")
        
        print(time.ctime()+"~~ Device "+device_id+':Killing background processes.')
        killAllBackgroundApps_cmd = 'adb -s '+device_id+' shell am kill-all'
        commandLine(killAllBackgroundApps_cmd).wait(30)
        
        print(time.ctime()+"~~ Device "+device_id+':Catching memory info after clear processes.')
        saveMemoryInfoAfterClearProcess_cmd = 'adb -s '+device_id+' shell dumpsys meminfo > ' + \
                                              saveMemInfoAfterClearProcess(create_time, device_id)
        commandLine(saveMemoryInfoAfterClearProcess_cmd).wait(30)
        
    else:
        print(time.ctime()+"~~ Device "+device_id+':Adb connection failed, please check and fix this.')

    print(time.ctime()+"~~ Device "+device_id+':Test finished.')
