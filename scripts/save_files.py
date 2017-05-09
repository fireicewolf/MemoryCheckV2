#coding=utf-8
import time

from scripts.create_dirctory import createadbLogsDir
from scripts.create_dirctory import createdumpsysLogsDir

def saveAdbLog(createtime,deviceid):
    adblogsdir=createadbLogsDir(createtime,deviceid)
    saveadblog=adblogsdir+'monkey_logs_'+time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime())+'.txt'
    return saveadblog

def saveMemInfoBeforeTest(createtime,deviceid):
    dumpsyslogsdir=createdumpsysLogsDir(createtime,deviceid)
    savememinfobeforetest=dumpsyslogsdir+'meminfo_before_test_'+time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime())+'.txt'
    return savememinfobeforetest

def saveMemInfo(createtime,deviceid):
    dumpsyslogsdir=createdumpsysLogsDir(createtime,deviceid)
    savememinfo=dumpsyslogsdir+'meminfo_'+time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime())+'.txt'
    return savememinfo

def saveMemInfoAfterClearProcess(createtime,deviceid):
    dumpsyslogsdir=createdumpsysLogsDir(createtime,deviceid)
    saveMemInfoAfterClearProcess=dumpsyslogsdir+'meminfo_after_clear_process_'+time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime())+'.txt'
    return saveMemInfoAfterClearProcess