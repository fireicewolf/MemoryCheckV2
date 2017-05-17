# coding=utf-8

import re
from .command_line import commandLine


# Definition for device lists
def deviceList():
    devices_cmd='adb devices'
    devices=commandLine(devices_cmd).stdout.read()
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


def adbstate(deviceid):
    adbstate_cmd='adb -s '+deviceid+' get-state'
    adbstate=commandLine(adbstate_cmd).stdout.read()
    adbstate=adbstate.decode()
    adbstate=adbstate.strip()
    return adbstate


# Definition for manufacture name
def manufacturer(deviceid):
    manufacturer_cmd='adb -s '+deviceid+' shell getprop ro.product.manufacturer'
    manufacturer=commandLine(manufacturer_cmd).stdout.read()
    manufacturer=manufacturer.decode()
    manufacturer=manufacturer.strip()
    return str(manufacturer)


# Definition for model name
def model(deviceid):
    model_cmd='adb -s '+deviceid+' shell getprop ro.product.model'
    model=commandLine(model_cmd).stdout.read()
    model=model.decode()
    model=model.strip()
    return str(model)


# Definition for build version
def buildVersion(deviceid):
    if manufacturer(deviceid)== "GIONEE":
        buildversion_cmd='adb -s '+deviceid+' shell getprop ro.gn.gnznvernumber'
        buildversion=commandLine(buildversion_cmd).stdout.read()
    else:
        buildversion_cmd='adb -s '+deviceid+' shell getprop ro.build.version.incremental'
        buildversion=commandLine(buildversion_cmd).stdout.read()
    buildversion=buildversion.decode()
    buildversion=buildversion.strip()
    return str(buildversion)