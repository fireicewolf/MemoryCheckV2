# coding=utf-8

import re
import time

from .command_line import commandLine


# Definition for device lists
def deviceList():
    devices_cmd = 'adb devices'
    devices = commandLine(devices_cmd).stdout.read()
    devices = devices.decode()
    devices = re.split('[\n\r]', devices)
    device_list = list()
    for line in devices:
        line = line.split("\t")
        if line[-1] == "device":
            device_list.append(line[0])
        if line[-1] == "offline":
            print("Device %s is offline, please check device status and reconnect it." % line[0])
        if line[-1] == "unauthorized":
            print("Device %s is unauthorized, please reconnect it and allow the USB debug permission." % line[0])
    return device_list


def adbstatus(device_id):
    adb_status_cmd = 'adb -s '+device_id+' get-state'
    adb_status = commandLine(adb_status_cmd).stdout.read()
    adb_status = adb_status.decode()
    adb_status = adb_status.strip()
    return adb_status


# Definition for manufacture name
def manufacturer(device_id):
    manufacturer_cmd = 'adb -s '+device_id+' shell getprop ro.product.manufacturer'
    manufacturer_name = commandLine(manufacturer_cmd).stdout.read()
    manufacturer_name = manufacturer_name.decode()
    manufacturer_name = manufacturer_name.strip()
    return str(manufacturer_name)


# Definition for model name
def model(device_id):
    model_cmd = 'adb -s '+device_id+' shell getprop ro.product.model'
    model_name = commandLine(model_cmd).stdout.read()
    model_name = model_name.decode()
    model_name = model_name.strip()
    return str(model_name)


# Definition for build version
def buildVersion(device_id):
    if manufacturer(device_id) == "GIONEE":
        build_version_cmd = 'adb -s '+device_id+' shell getprop ro.gn.gnznvernumber'
        build_version_code = commandLine(build_version_cmd).stdout.read()
    else:
        build_version_cmd = 'adb -s '+device_id+' shell getprop ro.build.version.incremental'
        build_version_code = commandLine(build_version_cmd).stdout.read()
    build_version_code = build_version_code.decode()
    build_version_code = build_version_code.strip()
    return str(build_version_code)


# Definition for screen resolution
def deviceScreenResolution(device_id):
    screenResolution_cmd = "adb -s " + device_id + " shell wm size"
    screenResolution = commandLine(screenResolution_cmd).stdout.read().strip()
    screenResolution = str(screenResolution)
    screenResolution = screenResolution.strip("b'Physical size: ")
    screenResolution = screenResolution.split('x')
    return screenResolution


# Definition for screen width
def deviceScreenWidth(device_id):
    deviceScreenWidth = deviceScreenResolution(device_id)[0]
    return int(deviceScreenWidth)


# Definition for screen height
def deviceScreenHeight(device_id):
    deviceScreenHeight = deviceScreenResolution(device_id)[1]
    return int(deviceScreenHeight)


def isScreenOn(device_id):
    checkIsScreenOn = commandLine('adb -s ' + device_id +
                                  ' shell "dumpsys window policy | grep mScreenOnFully"').stdout.read().strip()
    if "mScreenOnEarly=true mScreenOnFully=true" in str(checkIsScreenOn):
        return True
    elif "mScreenOnEarly=false mScreenOnFully=false" in str(checkIsScreenOn):
        return False
    else:
        print(time.ctime() + "~~ Device " + device_id + ':Get screen statues failed.')


def screenOn(device_id):
    if not isScreenOn(device_id):
        commandLine("adb -s " + device_id + " shell input keyevent KEYCODE_POWER").wait(10)


def screenOff(device_id):
    if isScreenOn(device_id):
        commandLine("adb -s " + device_id + " shell input keyevent KEYCODE_POWER").wait(10)
