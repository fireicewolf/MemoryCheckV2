#coding=utf-8
#Memory Check Ver 2.0

import os
import time
import subprocess
import re
import xlsxwriter
import threading

#Definition for device lists
def DeviceList():
    devices=subprocess.Popen('adb devices',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read()
    devices=devices.decode()
    devices=re.split('\n|\r',devices)
    deviceList=list()
    for line in devices:
        line=line.split("\t")
        if line[-1]=="device":
            deviceList.append(line[0])
        if line[-1]=="offline":
            print("Device %s is offline, please check device status and reconnect it."%line[0])
        if line[-1]=="unauthorized":
            print("Device %s is unauthorized, please reconnect it and allow the USB debug permission."%line[0])
    return deviceList

#Definition for manufacture name
def Manufacturer(deviceid):
    manufacturer=subprocess.Popen('adb -s '+deviceid+' shell getprop ro.product.manufacturer',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read()
    manufacturer=manufacturer.decode()
    manufacturer=manufacturer.strip()
    return str(manufacturer)
    
#Definition for model name
def Model(deviceid):
    model=subprocess.Popen('adb -s '+deviceid+' shell getprop ro.product.model',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read()
    model=model.decode()
    model=model.strip()
    return str(model)

#Definition for build version
def BuildVersion(deviceid):
    if Manufacturer(deviceid)== "GIONEE":
        buildversion=subprocess.Popen('adb -s '+deviceid+' shell getprop ro.gn.gnznvernumber',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read()
    else:
        buildversion=subprocess.Popen('adb -s '+deviceid+' shell getprop ro.build.version.incremental',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read()
    buildversion=buildversion.decode()
    buildversion=buildversion.strip()
    return str(buildversion)

#Definition for result directory 
def createResultDir(createtime):
    resultpath=("..\\Result")
    resultpathisExists=os.path.exists(resultpath)
    if not resultpathisExists:
        os.makedirs(resultpath)
    resultFolder=resultpath+os.path.sep+createtime
    resultFolderIsExists=os.path.exists(resultFolder)
    if not resultFolderIsExists:
        os.makedirs(resultFolder)
    return resultFolder+os.path.sep

createtime=time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime())
resultDir=createResultDir(createtime)

#Definition for adb logs directory
def createadbLogsDir(deviceid):
    logpath=resultDir
    logpathisExists=os.path.exists(logpath)
    if not logpathisExists:
        os.makedirs(logpath)
    logFolder=logpath+os.path.sep+"adb_logs"+os.path.sep+Manufacturer(deviceid)+'_'+Model(deviceid)+'_'+deviceid
    logFolderIsExists=os.path.exists(logFolder)
    if not logFolderIsExists:
        os.makedirs(logFolder)
    return logFolder+os.path.sep

#Definition for dumpsys logs directory
def createdumpsysLogsDir(deviceid):
    logpath=resultDir
    logpathisExists=os.path.exists(logpath)
    if not logpathisExists:
        os.makedirs(logpath)
    logFolder=logpath+os.path.sep+"dumpsys_logs"+os.path.sep+Manufacturer(deviceid)+'_'+Model(deviceid)+'_'+deviceid
    logFolderIsExists=os.path.exists(logFolder)
    if not logFolderIsExists:
        os.makedirs(logFolder)
    return logFolder+os.path.sep

#Definition for the save place of package names list
def createpackageListDir(deviceid):
    packagelistpath=resultDir
    packagelistpathisExists=os.path.exists(packagelistpath)
    if not packagelistpathisExists:
        os.makedirs(packagelistpath)
    packageListDir=packagelistpath+os.path.sep+"packages_names_list"+os.path.sep+Manufacturer(deviceid)+'_'+Model(deviceid)+'_'+deviceid
    packageListDirIsExists=os.path.exists(packageListDir)
    if not packageListDirIsExists:
        os.makedirs(packageListDir)
    return packageListDir+os.path.sep

#Definition for getting apps package names
def getAppPackageName(deviceid):
    subprocess.Popen('adb -s '+deviceid+' install -r -g package_name_viewer.apk',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).wait()
    subprocess.Popen('adb -s '+deviceid+' shell am start -n com.gionee.packages/com.gionee.packages.MainActivity',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).wait()
    subprocess.Popen('adb -s '+deviceid+' pull /sdcard/packages_visual.txt '+createpackageListDir(deviceid)+'packages_names_list.txt',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).wait()
    subprocess.Popen('adb -s '+deviceid+' uninstall com.gionee.packages',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).wait()
    subprocess.Popen('adb -s '+deviceid+' shell rm /sdcard/packages_visual.txt',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).wait()
    print(time.ctime()+"~~ Device "+deviceid+":Get app's package names success.")
    
    openapplists=open(createpackageListDir(deviceid)+'packages_names_list.txt','r')
    applists=openapplists.readlines()
    openapplists.close()
    
    print(time.ctime()+"~~ Device "+deviceid+':App lists load successfully，total '+str(len(applists))+' apps.')
    testpackages=''
    
    for line in applists:
        line=line.strip('\n')
        testpackages +='-p '+line+' '
        
    return testpackages

def adbstate(deviceid):
    adbstate=subprocess.Popen('adb -s '+deviceid+' get-state',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read()
    adbstate=adbstate.decode()
    adbstate=adbstate.strip()
    return adbstate

def saveAdbLog(deviceid):
    adblogsdir=createadbLogsDir(deviceid)
    saveadblog=adblogsdir+'monkey_logs_'+time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime())+'.txt'
    return saveadblog

def saveMemInfoBeforeTest(deviceid):
    dumpsyslogsdir=createdumpsysLogsDir(deviceid)
    savememinfobeforetest=dumpsyslogsdir+'meminfo_before_test_'+time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime())+'.txt'
    return savememinfobeforetest

def saveMemInfo(deviceid):
    dumpsyslogsdir=createdumpsysLogsDir(deviceid)
    savememinfo=dumpsyslogsdir+'meminfo_'+time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime())+'.txt'
    return savememinfo

def saveMemInfoAfterClearProcess(deviceid):
    dumpsyslogsdir=createdumpsysLogsDir(deviceid)
    saveMemInfoAfterClearProcess=dumpsyslogsdir+'meminfo_after_clear_process_'+time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime())+'.txt'
    return saveMemInfoAfterClearProcess

# def monkeyTestStatus(deviceid):
#     MonkeyTestProcess=subprocess.Popen('adb -s '+deviceid+' shell "ps | grep monkey"',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read()
#     MonkeyTestProcess=MonkeyTestProcess.decode()
#     MonkeyTestProcess=MonkeyTestProcess.split()
#     return MonkeyTestProcess

def killMonkeyTestProcess(deviceid):
    MonkeyTestProcess=subprocess.Popen('adb -s '+deviceid+' shell "ps | grep monkey"',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read()
    MonkeyTestProcess=MonkeyTestProcess.decode()
    MonkeyTestProcess=MonkeyTestProcess.split(' ')[5]
    subprocess.Popen('adb -s '+deviceid+' shell kill '+str(MonkeyTestProcess),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).wait()
        
#Definition for result save
def monkeytest(deviceid,runtime,gettime):
    testpackagenames=getAppPackageName(deviceid)  
    
    print(time.ctime()+"~~ Device "+deviceid+':Rebooting, please wait.')
    subprocess.Popen('adb -s '+deviceid+' reboot',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).wait()
    time.sleep(90)
    
    count=int(runtime*60*60*1000/500)
    if adbstate(deviceid)=="device":
        print(time.ctime()+"~~ Device "+deviceid+':Adb connection successful, wait 5 minutes before test')
        time.sleep(300)
        
        print(time.ctime()+"~~ Device "+deviceid+':Catching memory info before test.')
        savememinfobeforetest=saveMemInfoBeforeTest(deviceid)
        subprocess.Popen('adb -s '+deviceid+' shell dumpsys meminfo > '+savememinfobeforetest,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).wait
         
        print(time.ctime()+"~~ Device "+deviceid+':Starting monkey test.')
        saveadblog=saveAdbLog(deviceid)
        monkey_cmd='adb -s '+deviceid+' shell monkey '+testpackagenames+'--throttle 500 --ignore-crashes --ignore-security-exceptions --ignore-timeouts --monitor-native-crashes -v -v '+str(count)+' > '+saveadblog
        subprocess.Popen(monkey_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)

        runcount=int(runtime/gettime)  
        for i in range(runcount):
    
            time.sleep(gettime*60)
                
            savememinfo=saveMemInfo(deviceid)
            print(time.ctime()+"~~ Device "+deviceid+':Catching memory info.')
            subprocess.Popen('adb -s '+deviceid+' shell dumpsys meminfo > '+savememinfo,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).wait
            
            print(time.ctime()+"~~ Device "+deviceid+':Killing monkey test process.')
            killMonkeyTestProcess(deviceid)
            
            print(time.ctime()+"~~ Device "+deviceid+':Monkey test process killed.')
            
            print(time.ctime()+"~~ Device "+deviceid+':Killing background processes.')
            subprocess.Popen('adb -s '+deviceid+' shell am kill-all',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).wait
            
            print(time.ctime()+"~~ Device "+deviceid+':Catching memory info after clear processes.')
            savememoinfoafterclearprocess=saveMemInfoAfterClearProcess(deviceid)
            subprocess.Popen('adb -s '+deviceid+' shell dumpsys meminfo > '+savememoinfoafterclearprocess,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).wait
    
            print(time.ctime()+"~~ Device "+deviceid+':Starting monkey test.')
            saveadblog=saveAdbLog(deviceid)
            monkey_cmd='adb -s '+deviceid+' shell monkey '+testpackagenames+'--throttle 500 --ignore-crashes --ignore-security-exceptions --ignore-timeouts --monitor-native-crashes -v -v '+str(count)+' > '+saveadblog
            subprocess.Popen(monkey_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        
        time.sleep(gettime*60)
        
        print(time.ctime()+"~~ Device "+deviceid+':Killing monkey test process.')
        killMonkeyTestProcess(deviceid)
        
        print(time.ctime()+"~~ Device "+deviceid+':Monkey test process killed.')
        
        print(time.ctime()+"~~ Device "+deviceid+':Killing background processes.')
        subprocess.Popen('adb -s '+deviceid+' shell am kill-all',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).wait
        
        print(time.ctime()+"~~ Device "+deviceid+':Catching memory info after clear processes.')
        subprocess.Popen('adb -s '+deviceid+' shell dumpsys meminfo > '+savememoinfoafterclearprocess,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).wait
        
    else:
        print(time.ctime()+"~~ Device "+deviceid+':Adb connection failed')
        os.system("pause")
    
    print(time.ctime()+"~~ Device "+deviceid+':Test finished.')


threads = []
 
for line in DeviceList():
    deviceid=str(line)
 
    runtime=10
    gettime=1
    
    t1 = threading.Thread(target=monkeytest,args=(deviceid,runtime,gettime,))
    threads.append(t1)
#     t2 = threading.Thread(target=dumpsyslogs,args=(deviceid,runtime,gettime,))
#     threads.append(t2)
      
if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
         
    for t in threads:
        t.join()
    
