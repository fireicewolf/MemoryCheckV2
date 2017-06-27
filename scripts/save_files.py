#coding=utf-8
import time

from .create_dirctory import createadbLogsDir
from .create_dirctory import createdumpsysLogsDir


def saveAdbLog(create_time, device_id):
    adblogsdir = createadbLogsDir(create_time, device_id)
    saveadblog = adblogsdir+'monkey_logs_'+time.strftime('%Y.%m.%d_%H-%M-%S', time.localtime())+'.txt'
    return saveadblog


def saveMemInfoBeforeTest(create_time, device_id):
    dumpsyslogsdir = createdumpsysLogsDir(create_time, device_id)
    save_mem_info_before_test = dumpsyslogsdir+'meminfo_before_test_'+time.strftime(
        '%Y.%m.%d_%H-%M-%S', time.localtime())+'.txt'
    return save_mem_info_before_test


def saveMemInfo(create_time, device_id):
    dumpsyslogsdir = createdumpsysLogsDir(create_time, device_id)
    save_mem_info = dumpsyslogsdir+'meminfo_before_clear_process_' + time.strftime(
        '%Y.%m.%d_%H-%M-%S', time.localtime())+'.txt'
    return save_mem_info


def saveMemInfoAfterClearProcess(create_time, device_id):
    dumpsyslogsdir = createdumpsysLogsDir(create_time, device_id)
    save_mem_info_after_clear_process = dumpsyslogsdir+'meminfo_after_clear_process_' + time.strftime(
        '%Y.%m.%d_%H-%M-%S', time.localtime())+'.txt'
    return save_mem_info_after_clear_process
