# coding=utf-8

import os
from .device_info import manufacturer
from .device_info import model
from .device_info import buildVersion


# Definition for result directory
def createResultDir(create_time):
    result_path = os.path.join(".", "Result")
    result_path_is_exists = os.path.exists(result_path)
    if not result_path_is_exists:
        os.makedirs(result_path)
    result_folder = result_path + os.path.sep + create_time
    result_folder_is_exists = os.path.exists(result_folder)
    if not result_folder_is_exists:
        os.makedirs(result_folder)
    return result_folder + os.path.sep


def deviceDirName(device_id):
    device_dir_name = device_id
    return device_dir_name


# Definition for adb logs directory
def createadbLogsDir(create_time, device_id):
    adb_log_path = createResultDir(create_time)
    adb_log_path_is_exists = os.path.exists(adb_log_path)
    if not adb_log_path_is_exists:
        os.makedirs(adb_log_path)
    adb_log_folder = adb_log_path + os.path.sep + "adb_logs" + os.path.sep + deviceDirName(device_id)
    adb_log_folder_is_exists = os.path.exists(adb_log_folder)
    if not adb_log_folder_is_exists:
        os.makedirs(adb_log_folder)
    return adb_log_folder + os.path.sep


# Definition for dumpsys logs directory
def createdumpsysLogsDir(create_time, device_id):
    memory_info_dir_path = createResultDir(create_time)
    memory_info_dir_path_is_exists = os.path.exists(memory_info_dir_path)
    if not memory_info_dir_path_is_exists:
        os.makedirs(memory_info_dir_path)
    memory_info_folder = memory_info_dir_path + os.path.sep + "dumpsys_logs" + os.path.sep + deviceDirName(device_id)
    memory_info_folder_is_exists = os.path.exists(memory_info_folder)
    if not memory_info_folder_is_exists:
        os.makedirs(memory_info_folder)
    return memory_info_folder + os.path.sep


# Definition for the save place of package names list
def createPackageListDir(create_time, device_id):
    package_list_path = createResultDir(create_time)
    package_list_path_is_exists = os.path.exists(package_list_path)
    if not package_list_path_is_exists:
        os.makedirs(package_list_path)
    package_list_dir = package_list_path + os.path.sep + "packages_names_list" + os.path.sep + deviceDirName(device_id)
    package_list_dir_is_exists = os.path.exists(package_list_dir)
    if not package_list_dir_is_exists:
        os.makedirs(package_list_dir)
    return package_list_dir + os.path.sep


# Definition for the save place of screenshots
def createScreenshotDir(create_time, device_id):
    screenshots_path = createResultDir(create_time)
    screenshots_path_is_exists = os.path.exists(screenshots_path)
    if not screenshots_path_is_exists:
        os.makedirs(screenshots_path)
    screenshots_dir = screenshots_path + os.path.sep + "screenshots" + os.path.sep + deviceDirName(device_id)
    screenshots_dir_is_exists = os.path.exists(screenshots_dir)
    if not screenshots_dir_is_exists:
        os.makedirs(screenshots_dir)
    return screenshots_dir + os.path.sep
