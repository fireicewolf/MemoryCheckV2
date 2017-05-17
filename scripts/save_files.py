#coding=utf-8
import time

from .create_dirctory import createadbLogsDir
from .create_dirctory import createdumpsysLogsDir


def saveAdbLog(create_time, device_id):
    adblogsdir=createadbLogsDir(create_time, device_id)
    saveadblog=adblogsdir+'monkey_logs_'+time.strftime('%Y.%m.%d_%H-%M-%S',time.localtime())+'.txt'
    return saveadblog


def saveMemInfoBeforeTest(create_time, device_id):
    dumpsyslogsdir=createdumpsysLogsDir(create_time, device_id)
    savememinfobeforetest=dumpsyslogsdir+'meminfo_before_test_'+time.strftime('%Y.%m.%d_%H-%M-%S',time.localtime())+'.txt'
    return savememinfobeforetest


def saveMemInfo(create_time,device_id):
    dumpsyslogsdir=createdumpsysLogsDir(create_time, device_id)
    savememinfo=dumpsyslogsdir+'meminfo_before_clear_process_'+time.strftime('%Y.%m.%d_%H-%M-%S',time.localtime())+'.txt'
    return savememinfo


def saveMemInfoAfterClearProcess(create_time, device_id):
    dumpsyslogsdir=createdumpsysLogsDir(create_time, device_id)
    saveMemInfoAfterClearProcess=dumpsyslogsdir+'meminfo_after_clear_process_'+time.strftime('%Y.%m.%d_%H-%M-%S',time.localtime())+'.txt'
    return saveMemInfoAfterClearProcess