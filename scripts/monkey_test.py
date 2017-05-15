#coding=utf-8
import os
import time

from scripts.command_line import commandLine

from scripts.create_dirctory import createpackageListDir

from scripts.device_info import adbstate

from scripts.save_files import saveAdbLog
from scripts.save_files import saveMemInfoBeforeTest
from scripts.save_files import saveMemInfo
from scripts.save_files import saveMemInfoAfterClearProcess
    
def getAppPackageName(createtime,deviceid):
    installViewApk_cmd='adb -s '+deviceid+' install -r -g package_name_viewer.apk'
    commandLine(installViewApk_cmd).wait(10)
    
    launchViewApk_cmd='adb -s '+deviceid+' shell am start -n com.gionee.packages/com.gionee.packages.MainActivity'
    commandLine(launchViewApk_cmd).wait(10)

    saveListToPC_cmd='adb -s '+deviceid+' pull /sdcard/packages_visual.txt '+createpackageListDir(createtime,deviceid)+'packages_names_list.txt'
    commandLine(saveListToPC_cmd).wait(10)
    
    uninstallViewApk_cmd='adb -s '+deviceid+' uninstall com.gionee.packages'
    commandLine(uninstallViewApk_cmd).wait(10)
    
    removeListInPhone_cmd='adb -s '+deviceid+' shell rm /sdcard/packages_visual.txt'
    commandLine(removeListInPhone_cmd).wait(10)

    print(time.ctime()+"~~ Device "+deviceid+":Get app's package names success.")
    
    openapplists=open(createpackageListDir(createtime,deviceid)+'packages_names_list.txt','r')
    applists=openapplists.readlines()
    openapplists.close()
    
    print(time.ctime()+"~~ Device "+deviceid+':App lists load successfully, total '+str(len(applists))+' apps.')
    
    testpackages=''
    
    for line in applists:
        line=line.strip('\n')
        testpackages +='-p '+line+' '
        
    return testpackages

def killMonkeyTestProcess(deviceid):
    viewMonkeyTestProcess_cmd='adb -s '+deviceid+' shell "ps | grep monkey"'
    MonkeyTestProcess=commandLine(viewMonkeyTestProcess_cmd).stdout.read()
    MonkeyTestProcess=MonkeyTestProcess.decode()
    MonkeyTestProcess=MonkeyTestProcess.split(' ')[5]
    
    killMonkeyTestProcess_cmd='adb -s '+deviceid+' shell kill '+str(MonkeyTestProcess)
    commandLine(killMonkeyTestProcess_cmd).wait(10)
        
#Definition for result save
def monkeytest(createtime,deviceid,testpackagenames,runtime,gettime):
#     testpackagenames=getAppPackageName(createtime,deviceid)  
    
    print(time.ctime()+"~~ Device "+deviceid+':Rebooting, please wait.')
    deviceReboot_cmd='adb -s '+deviceid+' reboot'
    commandLine(deviceReboot_cmd).wait(10)
    adbWaitForDevice_cmd='adb -s '+deviceid+' wait-for-device'
    commandLine(adbWaitForDevice_cmd).wait(60)

    print(time.ctime()+"~~ Device "+deviceid+':Wait 30s for device stable.')
    time.sleep(30)
    
    count=int(runtime*60*60*1000/500)
    
    if adbstate(deviceid)=="device":
        print(time.ctime()+"~~ Device "+deviceid+':Adb connection successful, wait for 5 minutes before test')
        time.sleep(300)
        
        print(time.ctime()+"~~ Device "+deviceid+':Catching memory info before test.')
        saveMemoryInfoBeforeTest='adb -s '+deviceid+' shell dumpsys meminfo > '+saveMemInfoBeforeTest(createtime,deviceid)
        commandLine(saveMemoryInfoBeforeTest).wait(30)
    
        print(time.ctime()+"~~ Device "+deviceid+':Starting monkey test.')
        monkey_cmd='adb -s '+deviceid+' shell monkey '+testpackagenames+'--throttle 500 --ignore-crashes --ignore-security-exceptions --ignore-timeouts --monitor-native-crashes -v -v '+str(count)+' > '+saveAdbLog(createtime,deviceid)
        commandLine(monkey_cmd)
    
        runcount=int(runtime/gettime)
        
        for i in range(runcount-1):
    
            time.sleep(gettime*60)
            
            print(time.ctime()+"~~ Device "+deviceid+':Catching memory info.')
            saveMemoryInfo_cmd='adb -s '+deviceid+' shell dumpsys meminfo > '+saveMemInfo(createtime,deviceid)
            commandLine(saveMemoryInfo_cmd).wait(30)
            try:
                print(time.ctime()+"~~ Device "+deviceid+':Killing monkey test process.')
                killMonkeyTestProcess(deviceid)
                print(time.ctime()+"~~ Device "+deviceid+':Monkey test process killed.')
            
            except:
                print(time.ctime()+"~~ Device "+deviceid+":Did not found monkey test process.")
                
            print(time.ctime()+"~~ Device "+deviceid+':Killing background processes.')
            killAllBackgroundApps_cmd='adb -s '+deviceid+' shell am kill-all'
            commandLine(killAllBackgroundApps_cmd).wait(30)
            
            print(time.ctime()+"~~ Device "+deviceid+':Catching memory info after clear processes.')
            saveMemoryInfoAfterClearProcess_cmd='adb -s '+deviceid+' shell dumpsys meminfo > '+saveMemInfoAfterClearProcess(createtime,deviceid)
            commandLine(saveMemoryInfoAfterClearProcess_cmd).wait(30)
    
            print(time.ctime()+"~~ Device "+deviceid+':Starting monkey test.')
            monkey_cmd='adb -s '+deviceid+' shell monkey '+testpackagenames+'--throttle 500 --ignore-crashes --ignore-security-exceptions --ignore-timeouts --monitor-native-crashes -v -v '+str(count)+' > '+saveAdbLog(createtime,deviceid)
            commandLine(monkey_cmd)
        
        time.sleep(gettime*60)
        
        print(time.ctime()+"~~ Device "+deviceid+':Catching memory info.')
        saveMemoryInfo_cmd='adb -s '+deviceid+' shell dumpsys meminfo > '+saveMemInfo(createtime,deviceid)
        commandLine(saveMemoryInfo_cmd).wait(30)
        
        try:
            print(time.ctime()+"~~ Device "+deviceid+':Killing monkey test process.')
            killMonkeyTestProcess(deviceid).wait(30)
            print(time.ctime()+"~~ Device "+deviceid+':Monkey test process killed.')
        
        except:
            print(time.ctime()+"~~ Device "+deviceid+":Did not found monkey test process.")
        
        print(time.ctime()+"~~ Device "+deviceid+':Killing background processes.')
        killAllBackgroundApps_cmd='adb -s '+deviceid+' shell am kill-all'
        commandLine(killAllBackgroundApps_cmd).wait(30)
        
        print(time.ctime()+"~~ Device "+deviceid+':Catching memory info after clear processes.')
        saveMemoryInfoAfterClearProcess_cmd='adb -s '+deviceid+' shell dumpsys meminfo > '+saveMemInfoAfterClearProcess(createtime,deviceid)
        commandLine(saveMemoryInfoAfterClearProcess_cmd).wait(30)
        
    else:
        print(time.ctime()+"~~ Device "+deviceid+':Adb connection failed, please check and fix this.')

    
    print(time.ctime()+"~~ Device "+deviceid+':Test finished.')