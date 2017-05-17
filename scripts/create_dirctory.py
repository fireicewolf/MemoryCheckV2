# coding=utf-8

import os
from .device_info import manufacturer
from .device_info import model
from .device_info import buildVersion


# Definition for result directory
def createResultDir(create_time):
    resultpath = ".\\Result"
    resultpathisExists = os.path.exists(resultpath)
    if not resultpathisExists:
        os.makedirs(resultpath)
    resultFolder = resultpath + os.path.sep + create_time
    resultFolderIsExists = os.path.exists(resultFolder)
    if not resultFolderIsExists:
        os.makedirs(resultFolder)
    return resultFolder + os.path.sep


def deviceDirName(device_id):
    deviceDirName = manufacturer(device_id) + '__' + model(device_id) + '__' + device_id + '__' + buildVersion(device_id)
    return deviceDirName


# Definition for adb logs directory
def createadbLogsDir(create_time, device_id):
    logpath = createResultDir(create_time)
    logpathisExists = os.path.exists(logpath)
    if not logpathisExists:
        os.makedirs(logpath)
    logFolder = logpath + os.path.sep + "adb_logs" + os.path.sep + deviceDirName(device_id)
    logFolderIsExists = os.path.exists(logFolder)
    if not logFolderIsExists:
        os.makedirs(logFolder)
    return logFolder + os.path.sep


# Definition for dumpsys logs directory
def createdumpsysLogsDir(create_time, device_id):
    logpath = createResultDir(create_time)
    logpathisExists = os.path.exists(logpath)
    if not logpathisExists:
        os.makedirs(logpath)
    logFolder = logpath + os.path.sep + "dumpsys_logs" + os.path.sep + deviceDirName(device_id)
    logFolderIsExists = os.path.exists(logFolder)
    if not logFolderIsExists:
        os.makedirs(logFolder)
    return logFolder + os.path.sep


# Definition for the save place of package names list
def createpackageListDir(create_time, device_id):
    packagelistpath = createResultDir(create_time)
    packagelistpathisExists = os.path.exists(packagelistpath)
    if not packagelistpathisExists:
        os.makedirs(packagelistpath)
    packageListDir = packagelistpath + os.path.sep + "packages_names_list" + os.path.sep + deviceDirName(device_id)
    packageListDirIsExists = os.path.exists(packageListDir)
    if not packageListDirIsExists:
        os.makedirs(packageListDir)
    return packageListDir + os.path.sep
