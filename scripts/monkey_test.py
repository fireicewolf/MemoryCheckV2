# coding=utf-8
import os
import random
import time
from datetime import datetime

from .command_line import commandLine
from .create_dirctory import createPackageListDir
from .device_info import adbstatus, model, manufacturer, deviceScreenWidth, deviceScreenHeight, screenOn, screenOff
from .save_files import saveAdbLog, saveMemInfoBeforeTest, saveMemInfoBeforeCleaningProcesses, \
    saveMemInfoAfterAutoClearProcess, saveMemInfoAfterManualClearProcess, saveScreenshots, saveDumpsysAfterWholeTest


def getAppPackageName(create_time, device_id):
    install_view_apk_cmd = 'adb -s ' + device_id + ' install -r package_name_viewer.apk'
    commandLine(install_view_apk_cmd).wait(30)

    launch_view_apk_cmd = 'adb -s ' + device_id +\
                          ' shell am start -n com.gionee.packages/com.gionee.packages.MainActivity'
    commandLine(launch_view_apk_cmd).wait(30)

    save_list_to_pc_cmd = 'adb -s ' + device_id + ' pull /sdcard/packages_visual.txt ' + \
                          createPackageListDir(create_time, device_id) + 'packages_names_list.txt'
    commandLine(save_list_to_pc_cmd).wait(30)

    uninstall_view_apk_cmd = 'adb -s ' + device_id + ' uninstall com.gionee.packages'
    commandLine(uninstall_view_apk_cmd).wait(30)

    print(time.ctime() + "~~ Device " + device_id + ": Get apps' package names success.")

    open_app_lists = open(createPackageListDir(create_time, device_id) + 'packages_names_list.txt', 'r')

    app_lists = open_app_lists.read().split('\n')
    app_lists.pop()

    print(time.ctime() + "~~ Device " + device_id + ': App lists load successfully, total ' + str(
        len(app_lists)) + ' apps.')

    remove_list_in_phone_cmd = 'adb -s ' + device_id + ' shell rm /sdcard/packages_visual.txt'
    commandLine(remove_list_in_phone_cmd).wait()
    return app_lists


def getAppPackageNameNew(manufacturer_path_name, model_path_name, device_id):
    package_list_dir = os.path.join(".", "Package lists", manufacturer_path_name, model_path_name)
    package_list_dir_is_exist = os.path.exists(package_list_dir)
    if not package_list_dir_is_exist:
        os.makedirs(package_list_dir)
        print(time.ctime() + "~~ Device " + device_id + ": Package list dir not found.")

    else:
        package_list = package_list_dir + os.path.sep + 'packages_names_list.txt'
        package_list_is_exist = os.path.exists(package_list)
        if package_list_is_exist:
            print(time.ctime() + "~~ Device " + device_id + ": Package list found.")
            open_app_lists = open(package_list, 'r')
            app_lists = open_app_lists.read().split('\n')
            app_lists.pop()

            print(time.ctime() + "~~ Device " + device_id + ': App lists load successfully, total ' + str(
                len(app_lists)) + ' apps.')
            return app_lists

        else:
            print(time.ctime() + "~~ Device " + device_id + ": Package list not exist, please add it to right path.")


def killMonkeyTestProcess(device_id):
    view_monkey_test_process_cmd = 'adb -s ' + device_id + ' shell "ps | grep monkey"'
    monkey_test_process = commandLine(view_monkey_test_process_cmd).stdout.read()
    monkey_test_process = monkey_test_process.decode()
    try:
        monkey_test_process = monkey_test_process.split(' ')[5]
    except:
        pass

    kill_monkey_test_process_cmd = 'adb -s ' + device_id + ' shell kill ' + str(monkey_test_process)
    try:
        print(time.ctime() + "~~ Device " + device_id + ': Killing monkey test process.')
        commandLine(kill_monkey_test_process_cmd)
        print(time.ctime() + "~~ Device " + device_id + ': Monkey test process killed.')

    except:
        print(time.ctime() + "~~ Device " + device_id + ": Did not found monkey test process.")


def killBackgroundProcess(device_id):
    screenWidth = deviceScreenWidth(device_id)
    screenHeight = deviceScreenHeight(device_id)
    test_model = model(device_id)
    test_manufacturer = manufacturer(device_id)

    tap_app_switch = 'adb -s ' + device_id + ' shell input keyevent KEYCODE_APP_SWITCH'

    if test_model == 'W909' or test_model == 'GIONEE W919':
        kill_all_background_apps_cmd = 'adb -s ' + device_id + ' shell input tap 360 1120'

    elif test_model == 'MHA-AL00':
        kill_all_background_apps_cmd = 'adb -s ' + device_id + ' shell input tap 540 1680'

    elif screenHeight/screenWidth == 2 and test_manufacturer == 'GIONEE':
        kill_all_background_apps_cmd = 'adb -s ' + device_id + ' shell input tap ' \
                                       + str(int(360 / 720 * screenWidth)) + ' ' + str(int(1170 / 1440 * screenHeight))
    else:
        kill_all_background_apps_cmd = 'adb -s ' + device_id + ' shell input tap '\
                                       + str(int(540 / 1080 * screenWidth)) + ' ' + str(int(1580 / 1920 * screenHeight))

    print(time.ctime() + "~~ Device " + device_id + ': Killing background processes.')
    commandLine(tap_app_switch).wait()
    time.sleep(2)
    commandLine(kill_all_background_apps_cmd)


# Definition for result save
def randomMonkeyTest(create_dir_time, device_id, test_package_names, event_interval, event_count, running_time,
                     catch_log_interval, is_screen_off, screen_off_time):
    screen_off_time = float(screen_off_time)
    tap_app_switch = 'adb -s ' + device_id + ' shell input keyevent KEYCODE_APP_SWITCH'
    takeScreenshot_cmd = "adb -s " + device_id + " shell screencap -p /sdcard/test.png"

    print(time.ctime() + "~~ Device " + device_id + ': Rebooting, please wait.')
    commandLine('adb -s ' + device_id + ' reboot').wait(20)

    try:
        commandLine('adb -s ' + device_id + ' wait-for-device').wait(90)
    except:
        print(time.ctime() + "~~ Device " + device_id + ': Connection timeout after 90s, test will not execute.')

    print(time.ctime() + "~~ Device " + device_id + ': Waiting 30s before device being stable.')
    time.sleep(30)

    if adbstatus(device_id) == "device":
        save_memory_info_cmd = 'adb -s ' + device_id + ' shell dumpsys meminfo > '
        monkey_cmd = 'adb -s ' + device_id + ' shell monkey ' + test_package_names + \
                     '--throttle ' + event_interval + ' --ignore-crashes --ignore-security-exceptions ' \
                                                      '--ignore-timeouts --monitor-native-crashes -v -v ' + \
                     str(event_count) + ' > '

        print(time.ctime() + "~~ Device " + device_id +
              ': Connection successful, waiting 10 minutes before catching memory info')
        time.sleep(600)

        print(time.ctime() + "~~ Device " + device_id + ': Catching memory info before test.')
        commandLine(save_memory_info_cmd + saveMemInfoBeforeTest(create_dir_time, device_id)).wait(30)

        print(time.ctime() + "~~ Device " + device_id + ': Starting monkey test.')
        commandLine(monkey_cmd + saveAdbLog(create_dir_time, device_id))

        if is_screen_off == "true":
            running_count = int(running_time / (catch_log_interval + screen_off_time))
        else:
            running_count = int(running_time / catch_log_interval)

        for i in range(running_count - 1):
            time.sleep(catch_log_interval * 60)
            killMonkeyTestProcess(device_id)

            print(time.ctime() + "~~ Device " + device_id + ': Catching memory info.')
            commandLine(save_memory_info_cmd + saveMemInfoBeforeCleaningProcesses(create_dir_time, device_id)).wait(20)

            killBackgroundProcess(device_id)

            print(time.ctime() + "~~ Device " + device_id + ': Catching memory info after clear processes.')
            commandLine(save_memory_info_cmd + saveMemInfoAfterManualClearProcess(create_dir_time, device_id)).wait(20)

            if is_screen_off == "true":
                print(time.ctime() + "~~ Device " + device_id + ':Screen will be off ' + str(screen_off_time) +
                      ' minutes.')
                screenOff(device_id)
                time.sleep(int(screen_off_time * 60))
                screenOn(device_id)

            print(time.ctime() + "~~ Device " + device_id + ': Starting monkey test.')
            commandLine(monkey_cmd + saveAdbLog(create_dir_time, device_id))

        time.sleep(catch_log_interval * 60)
        killMonkeyTestProcess(device_id)

        print(time.ctime() + "~~ Device " + device_id + ': Catching memory info.')
        commandLine(save_memory_info_cmd + saveMemInfoBeforeCleaningProcesses(create_dir_time, device_id)).wait(30)

        killBackgroundProcess(device_id)

        print(time.ctime() + "~~ Device " + device_id + ': Checking background process')
        commandLine(tap_app_switch).wait(20)
        time.sleep(2)
        commandLine(takeScreenshot_cmd).wait(20)
        commandLine('adb -s ' + device_id + ' pull /sdcard/test.png ' +
                    saveScreenshots("After_manually_cleaning_processes_", create_dir_time, device_id)).wait(20)
        commandLine('adb -s ' + device_id + ' shell input keyevent KEYCODE_HOME').wait(20)
        print(time.ctime() + "~~ Device " + device_id + ': Screenshot saved.')

        print(time.ctime() + "~~ Device " + device_id + ': Catching memory info after whole test.')
        commandLine(save_memory_info_cmd + saveMemInfoAfterManualClearProcess(create_dir_time, device_id)).wait(30)
    else:
        print(time.ctime() + "~~ Device " + device_id + ': Connection failed, please check and fix this.')
    print(time.ctime() + "~~ Device " + device_id + ': Test finished.')


def sequenceMonkeyTest(create_dir_time, device_id, test_package_names, rounds, running_time, event_interval, event_count,
                       is_screen_off, screen_off_time):
    screen_off_time = float(screen_off_time)

    tap_app_switch = 'adb -s ' + device_id + ' shell input keyevent KEYCODE_APP_SWITCH'
    take_screenshot_cmd = "adb -s " + device_id + " shell screencap -p /sdcard/test.png"

    print(time.ctime() + "~~ Device " + device_id + ': Rebooting, please wait.')
    commandLine('adb -s ' + device_id + ' reboot').wait()

    try:
        commandLine('adb -s ' + device_id + ' wait-for-device').wait(90)
    except:
        print(time.ctime() + "~~ Device " + device_id + ': Connection timeout after 90s, test will not execute.')

    print(time.ctime() + "~~ Device " + device_id + ': Waiting 30s before device being stable.')
    time.sleep(30)

    if adbstatus(device_id) == "device":
        save_memory_info_cmd = 'adb -s ' + device_id + ' shell dumpsys meminfo > '
        save_dumpsys_cmd = 'adb -s ' + device_id + ' shell dumpsys > '

        print(time.ctime() + "~~ Device " + device_id +
              ': Connection successful, waiting 10 minutes before catching memory info')
        time.sleep(600)

        print(time.ctime() + "~~ Device " + device_id + ': Catching memory info before test.')
        commandLine(save_memory_info_cmd + saveMemInfoBeforeTest(create_dir_time, device_id)).wait(20)

        print(time.ctime() + "~~ Device " + device_id + ': Checking background process')
        commandLine(tap_app_switch).wait(10)
        time.sleep(2)
        commandLine(take_screenshot_cmd).wait(10)
        commandLine('adb -s ' + device_id + ' pull /sdcard/test.png ' +
                    saveScreenshots("Before_test_", create_dir_time, device_id)).wait(20)
        commandLine('adb -s ' + device_id + ' shell input keyevent KEYCODE_HOME').wait(20)
        print(time.ctime() + "~~ Device " + device_id + ': Screenshot saved.')

        for roundNum in range(int(rounds)):
            print(time.ctime() + "~~ Device " + device_id + ': Test round ' + str(roundNum+1) + '.')
            start_time = datetime.now()
            print(time.ctime() + "~~ Device " + device_id + ': Test will run for ' + str(running_time) + ' minutes.')
            print(time.ctime() + "~~ Device " + device_id + ': Starting monkey test.')

            for i in range(len(test_package_names)):
                test_package = random.choice(test_package_names)
                print(time.ctime() + "~~ Device " + device_id + ': App: "' + str(test_package) + '" test start.')
                monkey_cmd = 'adb -s ' + device_id + ' shell monkey -p ' + str(test_package) + \
                             ' --throttle ' + str(event_interval) + ' --ignore-crashes --ignore-security-exceptions ' \
                                                                    '--ignore-timeouts --monitor-native-crashes ' \
                                                                    '-v -v -v ' \
                             + str(event_count) + ' > '
                if (datetime.now() - start_time).seconds < int(running_time) * 60:
                    commandLine(monkey_cmd + saveAdbLog(test_package + '_', create_dir_time, device_id))
                    time.sleep(600)
                    killMonkeyTestProcess(device_id)

                    print(time.ctime() + "~~ Device " + device_id + ': App: "' + str(test_package) +
                          '" test end, back to home screen.')
                    commandLine('adb -s ' + device_id + ' shell input keyevent KEYCODE_HOME').wait(20)

                    if is_screen_off == 'true':
                        print(time.ctime() + "~~ Device " + device_id + ': Screen will be off ' + str(screen_off_time) +
                              ' minutes.')
                        screenOff(device_id)
                        time.sleep(int(screen_off_time * 60))
                        screenOn(device_id)
                    else:
                        time.sleep(int(screen_off_time * 60))
                else:
                    break

            killMonkeyTestProcess(device_id)
            time.sleep(300)

            print(time.ctime() + "~~ Device " + device_id + ': Catching memory info after monkey test.')
            commandLine(save_memory_info_cmd + saveMemInfoBeforeCleaningProcesses(create_dir_time, device_id)).wait(30)
            time.sleep(60)

            print(time.ctime() + "~~ Device " + device_id + ': Checking background process')
            commandLine(tap_app_switch).wait(20)
            time.sleep(2)
            commandLine(take_screenshot_cmd).wait(20)
            commandLine('adb -s ' + device_id + ' pull /sdcard/test.png ' +
                        saveScreenshots("After_monkey_test_processes_", create_dir_time, device_id)).wait(20)
            commandLine('adb -s ' + device_id + ' shell input keyevent KEYCODE_HOME').wait(10)
            print(time.ctime() + "~~ Device " + device_id + ': Screenshot saved.')

            print(time.ctime() + "~~ Device " + device_id + ': Device will be screen off for 30 minutes, '
                                                            'processes will be auto cleaned by system.')
            screenOff(device_id)
            time.sleep(1800)
            print(time.ctime() + "~~ Device " + device_id + ': Catching memory info after auto clean processes')
            commandLine(save_memory_info_cmd + saveMemInfoAfterAutoClearProcess(create_dir_time, device_id)).wait(30)

            screenOn(device_id)
            print(time.ctime() + "~~ Device " + device_id + ': Checking background process')
            commandLine(tap_app_switch).wait(20)
            time.sleep(2)
            commandLine(take_screenshot_cmd).wait(20)
            commandLine('adb -s ' + device_id + ' pull /sdcard/test.png ' +
                        saveScreenshots("After_automatically_cleaning_processes_", create_dir_time, device_id)).wait(20)
            commandLine('adb -s ' + device_id + ' shell input keyevent KEYCODE_HOME').wait(20)
            print(time.ctime() + "~~ Device " + device_id + ': Screenshot saved.')

            print(time.ctime() + "~~ Device " + device_id + ': Device will be screen on and stay idle for 30 minutes')
            time.sleep(1800)

            killBackgroundProcess(device_id)
            print(time.ctime() + "~~ Device " + device_id + ': Background processes has been cleaned, wait 1 minutes.')
            time.sleep(60)

            print(time.ctime() + "~~ Device " + device_id + ': Catching memory info after manual clean processes.')
            commandLine(save_memory_info_cmd + saveMemInfoAfterManualClearProcess(create_dir_time, device_id)).wait(30)
            time.sleep(60)

            print(time.ctime() + "~~ Device " + device_id + ': Checking background process')
            commandLine(tap_app_switch).wait(20)
            time.sleep(2)
            commandLine(take_screenshot_cmd).wait(20)
            commandLine('adb -s ' + device_id + ' pull /sdcard/test.png ' +
                        saveScreenshots("After_manually_cleaning_processes_", create_dir_time, device_id)).wait(20)
            commandLine('adb -s ' + device_id + ' shell input keyevent KEYCODE_HOME').wait(20)
            print(time.ctime() + "~~ Device " + device_id + ': Screenshot saved.')

            print(time.ctime() + "~~ Device " + device_id + ': Catching dumpsys info.')
            commandLine(save_dumpsys_cmd + saveDumpsysAfterWholeTest(create_dir_time, device_id)).wait(60)

    else:
        print(time.ctime() + "~~ Device " + device_id + ': Connection failed, please check and fix this.')
