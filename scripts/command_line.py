# coding=utf-8

import subprocess


def commandLine(command):
    command_line = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return command_line
