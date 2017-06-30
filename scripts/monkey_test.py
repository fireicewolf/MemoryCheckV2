#coding=utf-8
import time
from datetime import datetime

from .command_line import commandLine

from .create_dirctory import createpackageListDir

from .device_info import adbstatus, model

from .save_files import saveAdbLog, saveMemInfoBeforeTest, saveMemInfo, saveMemInfoAfterClearProcess, \
    saveMemInfoAfterWholeTest
from .device_info import deviceScreenWidth, deviceScreenHeight, screenOn, screenOff


def getAppPackageName(create_time, device_id):
    install_view_apk_cmd = 'adb -s '+device_id+' install -r package_name_viewer.apk'
    commandLine(install_view_apk_cmd).wait(10)

    launch_view_apk_cmd = 'adb -s '+device_id+' shell am start -n com.gionee.packages/com.gionee.packages.MainActivity'
    commandLine(launch_view_apk_cmd).wait(10)

    save_list_to_pc_cmd = 'adb -s '+device_id+' pull /sdcard/packages_visual.txt ' + \
                          createpackageListDir(create_time, device_id)+'packages_names_list.txt'
    commandLine(save_list_to_pc_cmd).wait(10)

    uninstall_view_apk_cmd = 'adb -s '+device_id+' uninstall com.gionee.packages'
    commandLine(uninstall_view_apk_cmd).wait(10)

    remove_list_in_phone_cmd = 'adb -s '+device_id+' shell rm /sdcard/packages_visual.txt'
    commandLine(remove_list_in_phone_cmd).wait(10)

    print(time.ctime()+"~~ Device "+device_id+":Get apps' package names success.")

    openapplists = open(createpackageListDir(create_time, device_id)+'packages_names_list.txt', 'r')
    applists = openapplists.read().split('\n')
    applists.pop()

    print(time.ctime()+"~~ Device "+device_id+':App lists load successfully, total '+str(len(applists))+' apps.')
    return applists


def killMonkeyTestProcess(device_id):
    view_monkey_test_process_cmd = 'adb -s '+device_id+' shell "ps | grep monkey"'
    monkey_test_process = commandLine(view_monkey_test_process_cmd).stdout.read()
    monkey_test_process = monkey_test_process.decode()
    try:
        monkey_test_process = monkey_test_process.split(' ')[5]
        kill_monkey_test_process_cmd = 'adb -s ' + device_id + ' shell kill ' + str(monkey_test_process)
    except:
        pass

    try:
        print(time.ctime() + "~~ Device " + device_id + ': Killing monkey test process.')
        commandLine(kill_monkey_test_process_cmd).wait(10)
        print(time.ctime() + "~~ Device " + device_id + ': Monkey test process killed.')

    except:
        print(time.ctime() + "~~ Device " + device_id + ": Did not found monkey test process.")


def killBackgroundProcess(device_id):
    screenWidth = deviceScreenWidth(device_id)
    screenHeight = deviceScreenHeight(device_id)

    if model(device_id) == 'W909':
        kill_all_background_apps_cmd = 'adb -s ' + device_id \
                                       + ' shell input keyevent KEYCODE_APP_SWITCH; input tap 360 1115'
    else:
        kill_all_background_apps_cmd = 'adb -s ' + device_id \
                                       + ' shell input keyevent KEYCODE_APP_SWITCH; input tap ' \
                                       + str(int(540 / 1080 * screenWidth)) + ' ' + str(int(1580 / 1920 * screenHeight))

    print(time.ctime() + "~~ Device " + device_id + ': Killing background processes.')
    commandLine(kill_all_background_apps_cmd).wait(30)


#Definition for result save
def randomMonkeyTest(create_dir_time, device_id, test_package_names, event_interval, event_count, running_time,
                     catch_log_interval, is_screen_off, screen_off_time):

    screen_off_time = float(screen_off_time)

    print(time.ctime()+"~~ Device "+device_id+': Rebooting, please wait.')
    commandLine('adb -s '+device_id+' reboot').wait(10)

    try:
        commandLine('adb -s ' + device_id + ' wait-for-device').wait(90)
    except:
        print(time.ctime()+"~~ Device "+device_id+': Connection timeout after 90s, test will not execute.')

    print(time.ctime()+"~~ Device "+device_id+': Waiting 30s before device being stable.')
    time.sleep(30)

    if adbstatus(device_id) == "device":
        save_memory_info_cmd = 'adb -s ' + device_id + ' shell dumpsys meminfo > '
        monkey_cmd = 'adb -s '+device_id+' shell monkey '+test_package_names + \
                     '--throttle ' + event_interval + ' --ignore-crashes --ignore-security-exceptions ' \
                     '--ignore-timeouts --monitor-native-crashes -v -v ' + \
                     str(event_count)+' > '

        print(time.ctime()+"~~ Device "+device_id +
              ': Connection successful, waiting 10 minutes before catching memory info')
        time.sleep(600)

        print(time.ctime()+"~~ Device "+device_id + ': Catching memory info before test.')
        commandLine(save_memory_info_cmd + saveMemInfoBeforeTest(create_dir_time, device_id)).wait(30)
    
        print(time.ctime()+"~~ Device "+device_id + ': Starting monkey test.')
        commandLine(monkey_cmd + saveAdbLog(create_dir_time, device_id))

        if is_screen_off == "true":
            running_count = int(running_time / (catch_log_interval + screen_off_time))
        else:
            running_count = int(running_time / catch_log_interval)
        
        for i in range(running_count-1):
            time.sleep(catch_log_interval * 60)
            killMonkeyTestProcess(device_id)

            print(time.ctime()+"~~ Device "+device_id+': Catching memory info.')
            commandLine(save_memory_info_cmd + saveMemInfo(create_dir_time, device_id)).wait(10)

            killBackgroundProcess(device_id)

            print(time.ctime()+"~~ Device "+device_id+': Catching memory info after clear processes.')
            commandLine(save_memory_info_cmd + saveMemInfoAfterClearProcess(create_dir_time, device_id)).wait(10)

            if is_screen_off == "true":
                print(time.ctime() + "~~ Device " + device_id + ':Screen will be off ' + str(screen_off_time) +
                      ' minutes.')
                screenOff(device_id)
                time.sleep(int(screen_off_time * 60))
                screenOn(device_id)
    
            print(time.ctime()+"~~ Device "+device_id+': Starting monkey test.')
            commandLine(monkey_cmd + saveAdbLog(create_dir_time, device_id))

        time.sleep(catch_log_interval*60)
        killMonkeyTestProcess(device_id)

        print(time.ctime()+"~~ Device "+device_id+': Catching memory info.')
        commandLine(save_memory_info_cmd + saveMemInfo(create_dir_time, device_id)).wait(30)

        killBackgroundProcess(device_id)
        
        print(time.ctime()+"~~ Device "+device_id+': Catching memory info after clearing processes.')
        commandLine(save_memory_info_cmd + saveMemInfoAfterClearProcess(create_dir_time, device_id)).wait(10)
    else:
        print(time.ctime()+"~~ Device "+device_id+': Connection failed, please check and fix this.')
    print(time.ctime()+"~~ Device "+device_id+': Test finished.')


def sequenceMonkeyTest(create_dir_time, device_id, test_package_names, running_time, event_interval, event_count,
                       is_screen_off, screen_off_time):

    screen_off_time = float(screen_off_time)

    print(time.ctime()+"~~ Device "+device_id+': Rebooting, please wait.')
    commandLine('adb -s '+device_id+' reboot').wait(10)

    try:
        commandLine('adb -s ' + device_id + ' wait-for-device').wait(90)
    except:
        print(time.ctime()+"~~ Device "+device_id+': Connection timeout after 90s, test will not execute.')

    time.sleep(30)
    print(time.ctime()+"~~ Device "+device_id+': Waiting 30s before device being stable.')

    if adbstatus(device_id) == "device":
        save_memory_info_cmd = 'adb -s ' + device_id + ' shell dumpsys meminfo > '

        print(time.ctime() + "~~ Device " + device_id +
              ': Connection successful, waiting 10 minutes before catching memory info')
        time.sleep(600)

        print(time.ctime() + "~~ Device " + device_id + ': Catching memory info before test.')
        commandLine(save_memory_info_cmd + saveMemInfoBeforeTest(create_dir_time, device_id)).wait(10)

        startTime = datetime.now()
        print(time.ctime() + "~~ Device " + device_id + ': Test will run for ' + str(running_time) + ' minutes.')

        print(time.ctime() + "~~ Device " + device_id + ': Starting monkey test.')
        for i in range(len(test_package_names)):
            testPackage = test_package_names.pop(0)
            print(time.ctime() + "~~ Device " + device_id + ': Start testing app: "' + str(testPackage) + '".')
            monkey_cmd = 'adb -s ' + device_id + ' shell monkey -p ' + str(testPackage) + \
                         ' --throttle ' + str(event_interval) + ' --ignore-crashes --ignore-security-exceptions ' \
                         '--ignore-timeouts --monitor-native-crashes -v -v -v ' + str(event_count) + ' > '
            if (datetime.now() - startTime).seconds < int(running_time) * 60:
                commandLine(monkey_cmd + saveAdbLog(testPackage+'_', create_dir_time, device_id)).wait()
                print(time.ctime() + "~~ Device " + device_id + ': App: "' + str(testPackage) +
                      '" test end, back to home screen.')
                commandLine('adb -s ' + device_id + ' shell input keyevent KEYCODE_HOME').wait(10)
                if is_screen_off == 'true':
                    print(time.ctime() + "~~ Device " + device_id + ': Screen will be off ' + str(screen_off_time) +
                          ' minutes.')
                    screenOff(device_id)
                    time.sleep(int(screen_off_time * 60))
                    screenOn(device_id)
            else:
                break

        killMonkeyTestProcess(device_id)
        time.sleep(60)

        save_memory_info_cmd = 'adb -s ' + device_id + ' shell dumpsys meminfo > '

        print(time.ctime() + "~~ Device " + device_id + ': Catching memory info.')
        commandLine(save_memory_info_cmd + saveMemInfo(create_dir_time, device_id)).wait(30)

        killBackgroundProcess(device_id)
        time.sleep(60)

        print(time.ctime() + "~~ Device " + device_id + ': Catching memory info after clear processes.')
        commandLine(save_memory_info_cmd + saveMemInfoAfterClearProcess(create_dir_time, device_id)).wait(10)

        print(time.ctime() + "~~ Device " + device_id + ': Rebooting, please wait.')
        commandLine('adb -s ' + device_id + ' reboot').wait(10)

        try:
            commandLine('adb -s ' + device_id + ' wait-for-device').wait(90)
        except:
            print(time.ctime() + "~~ Device " + device_id + ': Connecting timeout after 90s, test will not execute.')

        print(time.ctime() + "~~ Device " + device_id + ': Wait 30s before device being stable.')
        time.sleep(30)

        print(time.ctime() + "~~ Device " + device_id +
              ': Connection successful, wait for 10 minutes before catching memory info')
        time.sleep(600)

        print(time.ctime() + "~~ Device " + device_id + ': Catching memory info after whole test finished.')
        commandLine(save_memory_info_cmd + saveMemInfoAfterWholeTest(create_dir_time, device_id)).wait(10)

    else:
        print(time.ctime() + "~~ Device "+device_id+': Connection failed, please check and fix this.')
