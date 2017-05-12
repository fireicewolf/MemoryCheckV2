#coding=utf-8
import os
from scripts.device_info import manufacturer
from scripts.device_info import model
from scripts.device_info import buildVersion

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

def deviceDirName(deviceid):
    deviceDirName=manufacturer(deviceid)+'__'+model(deviceid)+'__'+deviceid+'__'+buildVersion(deviceid)
    return deviceDirName

#Definition for adb logs directory
def createadbLogsDir(createtime,deviceid):
    logpath=createResultDir(createtime)
    logpathisExists=os.path.exists(logpath)
    if not logpathisExists:
        os.makedirs(logpath)
    logFolder=logpath+os.path.sep+"adb_logs"+os.path.sep+deviceDirName(deviceid)
    logFolderIsExists=os.path.exists(logFolder)
    if not logFolderIsExists:
        os.makedirs(logFolder)
    return logFolder+os.path.sep

#Definition for dumpsys logs directory
def createdumpsysLogsDir(createtime,deviceid):
    logpath=createResultDir(createtime)
    logpathisExists=os.path.exists(logpath)
    if not logpathisExists:
        os.makedirs(logpath)
    logFolder=logpath+os.path.sep+"dumpsys_logs"+os.path.sep+deviceDirName(deviceid)
    logFolderIsExists=os.path.exists(logFolder)
    if not logFolderIsExists:
        os.makedirs(logFolder)
    return logFolder+os.path.sep

#Definition for the save place of package names list
def createpackageListDir(createtime,deviceid):
    packagelistpath=createResultDir(createtime)
    packagelistpathisExists=os.path.exists(packagelistpath)
    if not packagelistpathisExists:
        os.makedirs(packagelistpath)
    packageListDir=packagelistpath+os.path.sep+"packages_names_list"+os.path.sep+deviceDirName(deviceid)
    packageListDirIsExists=os.path.exists(packageListDir)
    if not packageListDirIsExists:
        os.makedirs(packageListDir)
    return packageListDir+os.path.sep