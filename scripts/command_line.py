#coding=utf-8
 
import subprocess
     
def commandLine(command):
    commandLine=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    return commandLine