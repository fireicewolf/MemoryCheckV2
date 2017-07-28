# coding=utf-8
import time

from .create_dirctory import createadbLogsDir, createdumpsysLogsDir, createScreenshotDir


def saveAdbLog(testPackage=None, create_time=None, device_id=None):
    adblogsdir = createadbLogsDir(create_time, device_id)
    saveadblog = adblogsdir + 'monkey_logs_' + testPackage + time.strftime('%Y.%m.%d_%H-%M-%S',
                                                                           time.localtime()) + '.txt'
    return saveadblog


def saveMemInfoBeforeTest(create_time, device_id):
    dumpsyslogsdir = createdumpsysLogsDir(create_time, device_id)
    save_mem_info_before_test = dumpsyslogsdir + 'meminfo_before_test_' + time.strftime('%Y.%m.%d_%H-%M-%S',
                                                                                        time.localtime()) + '.txt'
    return save_mem_info_before_test


def saveMemInfo(create_time, device_id):
    dumpsyslogsdir = createdumpsysLogsDir(create_time, device_id)
    save_mem_info = dumpsyslogsdir + 'meminfo_before_clear_process_' + time.strftime('%Y.%m.%d_%H-%M-%S',
                                                                                     time.localtime()) + '.txt'
    return save_mem_info


def saveMemInfoAfterClearProcess(create_time, device_id):
    dumpsyslogsdir = createdumpsysLogsDir(create_time, device_id)
    save_mem_info_after_clear_process = dumpsyslogsdir + 'meminfo_after_clear_process_' + time.strftime(
        '%Y.%m.%d_%H-%M-%S', time.localtime()) + '.txt'
    return save_mem_info_after_clear_process


def saveDumpsysAfterWholeTest(create_time, device_id):
    dumpsyslogsdir = createdumpsysLogsDir(create_time, device_id)
    save_mem_info_after_whole_test = dumpsyslogsdir + 'dumpsys_after_whole_test_' + time.strftime(
        '%Y.%m.%d_%H-%M-%S', time.localtime()) + '.txt'
    return save_mem_info_after_whole_test


def saveScreenshots(create_time, device_id):
    dumpsyslogsdir = createScreenshotDir(create_time, device_id)
    save_screenshot = dumpsyslogsdir + 'screenshot_' + time.strftime('%Y.%m.%d_%H-%M-%S', time.localtime()) + '.png'
    return save_screenshot
