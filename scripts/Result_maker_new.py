# coding=utf-8

import os
import time
import xlsxwriter


def resultMakerNew(save_path, remix_test_packages, monkey_test_time, monkey_event_interval, monkey_event_count):
    global free_ram_after_cleaning_processes, used_ram_after_cleaning_processes, \
        free_ram_before_cleaning_processes, used_ram_before_cleaning_processes, \
        total_ram_before_test, used_ram_before_test, free_ram_before_test, \
        used_ram_after_whole_test, total_ram_after_whole_test, free_ram_after_whole_test

    memory_info_dir = save_path + 'dumpsys_logs'
    result_name = save_path + "Test Result_" + time.strftime('%Y.%m.%d_%H-%M-%S', time.localtime()) + ".xlsx"

    print(time.ctime() + "~~ Saving test result: " + result_name)

    workbook = xlsxwriter.Workbook(result_name)

    big_blue_title_format = workbook.add_format({'font_name': 'Arial', 'font_size': 18, 'bold': True,
                                                 'bg_color': '#4472C4', 'align': 'center', 'valign': 'vcenter',
                                                 'border': 1})

    yellow_title_format = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'align': 'center',
                                               'valign': 'vcenter', 'border': 1, 'bg_color': '#FFC000',
                                               'bold': True})

    light_blue_format = workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                             'valign': 'vcenter', 'border': 1, 'bg_color': '#BDD7EE'})

    light_green_format = workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                              'valign': 'vcenter', 'border': 1, 'bg_color': '#92D050', 'bold': True})

    light_grey_format = workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                             'valign': 'vcenter', 'border': 1, 'bg_color': '#C9C9C9'})

    orange_format = workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                         'valign': 'vcenter', 'border': 1, 'bg_color': '#F4B084', 'bold': True})

    blue_format = workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                       'valign': 'vcenter', 'border': 1, 'bg_color': '#00B0F0', 'bold': True})

    grey_format = workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                       'valign': 'vcenter', 'border': 1, 'bg_color': '#808080', 'bold': True})

    default_cell_format = workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                               'valign': 'vcenter', 'border': 1})

    num_cell_format = workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                           'valign': 'vcenter', 'border': 1, 'num_format': '0.00'})

    process_name_cell_format = workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'valign': 'vcenter',
                                                    'border': 1})

    for dirpath, dir_names, file_names in os.walk(memory_info_dir):
        for dir_name in dir_names:
            get_name = dir_name.split("__")

            manufacturer = get_name[0]
            model = get_name[1]
            device_id = get_name[2]
            build_version = get_name[3]

            worksheet = workbook.add_worksheet(model + ' ' + device_id)

            worksheet.merge_range('A1:F1', 'Memory Usage Test', big_blue_title_format)

            worksheet.merge_range('A2:B2', 'Device Info', yellow_title_format)
            worksheet.write('A3', 'Manufacturer', light_blue_format)
            worksheet.write('A4', 'Model', light_blue_format)
            worksheet.write('A5', 'Device', light_blue_format)
            worksheet.write('A6', 'Build Version', light_blue_format)

            worksheet.write('B3', manufacturer, default_cell_format)
            worksheet.write('B4', model, default_cell_format)
            worksheet.write('B5', device_id, default_cell_format)
            worksheet.write('B6', build_version, default_cell_format)

            worksheet.merge_range('C2:D2', 'Test Config', yellow_title_format)
            worksheet.write('C3', 'Remix Test Packages', light_blue_format)
            worksheet.write('C4', 'Monkey Test Time (min)', light_blue_format)
            worksheet.write('C5', 'Monkey Event Interval (ms)', light_blue_format)
            worksheet.write('C6', 'Monkey Event Count', light_blue_format)

            worksheet.write('D3', remix_test_packages, default_cell_format)
            worksheet.write('D4', monkey_test_time, default_cell_format)
            worksheet.write('D5', monkey_event_interval, default_cell_format)
            worksheet.write('D6', monkey_event_count, default_cell_format)

            worksheet.merge_range('A7:F7', 'Test Result', yellow_title_format)

            memory_info_before_clear_process_list = list()
            memory_info_after_clear_process_list = list()

            for result_dirpath, result_dir_names, result_file_names in os.walk(
                                    memory_info_dir + os.path.sep + dir_name):
                for result_file_name in result_file_names:
                    if result_file_name.startswith('meminfo_before_test_'):
                        get_memory_info_time = result_file_name.strip('meminfo_before_test_|.txt')
                        get_memory_info_time = get_memory_info_time.replace('_', ' ')
                        get_memory_info_time = get_memory_info_time.replace('-', ':')

                        with open(memory_info_dir + os.path.sep + dir_name + os.path.sep + result_file_name, 'r') as f:
                            file = f.readlines()

                        for line in file:
                            if "Total RAM:" in line:
                                line = line.strip('Total RAM: ')
                                line = line.split('kB')
                                total_ram_before_test = float(int(line[0]) / 1000)
                            if "Free RAM:" in line:
                                line = line.strip('Free RAM: ')
                                line = line.split('kB')
                                free_ram_before_test = float(int(line[0]) / 1000)
                            if "Used RAM:" in line:
                                line = line.strip('Used RAM: ')
                                line = line.split('kB')
                                used_ram_before_test = float(int(line[0]) / 1000)

                        worksheet.merge_range('E2:F2', 'Memory Info Before Test (After Reboot)', yellow_title_format)
                        worksheet.write('E3', 'Test Time', light_blue_format)
                        worksheet.write('E4', 'Total RAM (MB)', light_blue_format)
                        worksheet.write('E5', 'Used RAM (MB)', light_blue_format)
                        worksheet.write('E6', 'Free RAM (MB)', light_blue_format)

                        worksheet.write('F3', get_memory_info_time, num_cell_format)
                        worksheet.write('F4', total_ram_before_test, num_cell_format)
                        worksheet.write('F5', used_ram_before_test, num_cell_format)
                        worksheet.write('F6', free_ram_before_test, num_cell_format)

                    # if result_file_name.startswith('meminfo_after_whole_test_'):
                    #     get_memory_info_time = result_file_name.strip('meminfo_after_whole_test_|.txt')
                    #     get_memory_info_time = get_memory_info_time.replace('_', ' ')
                    #     get_memory_info_time = get_memory_info_time.replace('-', ':')
                    #
                    #     with open(memory_info_dir + os.path.sep + dir_name + os.path.sep + result_file_name, 'r')
                    # as f:
                    #         file = f.readlines()
                    #
                    #     for line in file:
                    #         if "Total RAM:" in line:
                    #             line = line.strip('Total RAM: ')
                    #             line = line.split('kB')
                    #             total_ram_after_whole_test = float(int(line[0]) / 1000)
                    #         if "Free RAM:" in line:
                    #             line = line.strip('Free RAM: ')
                    #             line = line.split('kB')
                    #             free_ram_after_whole_test = float(int(line[0]) / 1000)
                    #         if "Used RAM:" in line:
                    #             line = line.strip('Used RAM: ')
                    #             line = line.split('kB')
                    #             used_ram_after_whole_test = float(int(line[0]) / 1000)
                    #
                    #     worksheet.merge_range('E2:F2', 'Memory Info After Test (After Reboot)', yellow_title_format)
                    #     worksheet.write('E3', 'Test Time', light_blue_format)
                    #     worksheet.write('E4', 'Total RAM (MB)', light_blue_format)
                    #     worksheet.write('E5', 'Used RAM (MB)', light_blue_format)
                    #     worksheet.write('E6', 'Free RAM (MB)', light_blue_format)
                    #
                    #     worksheet.write('F3', get_memory_info_time, default_cell_format)
                    #     worksheet.write('F4', total_ram_after_whole_test, default_cell_format)
                    #     worksheet.write('F5', used_ram_after_whole_test, default_cell_format)
                    #     worksheet.write('F6', free_ram_after_whole_test, default_cell_format)

                    if result_file_name.startswith('meminfo_before_clear_process_'):
                        memory_info_before_clear_process_list.append(result_file_name)

                    if result_file_name.startswith('meminfo_after_clear_process_'):
                        memory_info_after_clear_process_list.append(result_file_name)

            for i in range(len(memory_info_before_clear_process_list)):
                round_row_num = 8 + i * 17

                worksheet.merge_range('A' + str(round_row_num) + ':F' + str(round_row_num), 'Round ' + str(i + 1),
                                      grey_format)
                worksheet.merge_range('A' + str(round_row_num + 1) + ':B' + str(round_row_num + 1),
                                      'Before cleaning background processes', orange_format)
                worksheet.write('A' + str(round_row_num + 2), 'Test Time', light_blue_format)
                worksheet.write('A' + str(round_row_num + 3), 'Used RAM (MB)', light_blue_format)
                worksheet.write('A' + str(round_row_num + 4), 'Free RAM (MB)', light_blue_format)
                worksheet.merge_range('A' + str(round_row_num + 5) + ':B' + str(round_row_num + 5),
                                      'Top 10 Processes Info', orange_format)
                worksheet.write('A' + str(round_row_num + 6), 'Package Name', light_blue_format)
                worksheet.write('B' + str(round_row_num + 6), 'Memory used (MB)', light_blue_format)

                filename = memory_info_before_clear_process_list[i]
                get_memory_info_time = filename.strip('meminfo_before_clear_process_|.txt')
                get_memory_info_time = get_memory_info_time.replace('_', ' ')
                get_memory_info_time = get_memory_info_time.replace('-', ':')

                with open(memory_info_dir + os.path.sep + dir_name + os.path.sep + filename, 'r') as f:
                    file = f.readlines()

                for line in file:
                    if "Free RAM:" in line:
                        line = line.strip('Free RAM (MB): ')
                        line = line.split('kB')
                        free_ram_before_cleaning_processes = float(int(line[0]) / 1000)
                    if "Used RAM:" in line:
                        line = line.strip('Used RAM (MB): ')
                        line = line.split('kB')
                        used_ram_before_cleaning_processes = float(int(line[0]) / 1000)

                worksheet.write('B' + str(round_row_num + 2), get_memory_info_time, default_cell_format)
                worksheet.write('B' + str(round_row_num + 3), used_ram_before_cleaning_processes, num_cell_format)
                worksheet.write('B' + str(round_row_num + 4), free_ram_before_cleaning_processes, num_cell_format)

                for a in range(8, 27, 2):
                    b = int(a / 2 - 4)
                    process_name = file[a].strip().split('kB: ')[1]
                    process_mem_usage = file[a].strip().split('kB: ')[0]
                    process_mem_usage = float(int(process_mem_usage) / 1000)
                    process_cell_row_num = str(15 + b + i * 17)

                    worksheet.write('A' + process_cell_row_num, process_name, process_name_cell_format)
                    worksheet.write('B' + process_cell_row_num, process_mem_usage, num_cell_format)

            for i in range(len(memory_info_after_clear_process_list)):
                round_row_num = 8 + i * 17

                worksheet.merge_range('C' + str(round_row_num + 1) + ':D' + str(round_row_num + 1),
                                      'After cleaning background processes', light_green_format)
                worksheet.write('C' + str(round_row_num + 2), 'Test Time', light_blue_format)
                worksheet.write('C' + str(round_row_num + 3), 'Used RAM (MB)', light_blue_format)
                worksheet.write('C' + str(round_row_num + 4), 'Free RAM (MB)', light_blue_format)
                worksheet.merge_range('C' + str(round_row_num + 5) + ':D' + str(round_row_num + 5),
                                      'Top 10 Processes Info', light_green_format)
                worksheet.write('C' + str(round_row_num + 6), 'Package Name', light_blue_format)
                worksheet.write('D' + str(round_row_num + 6), 'Memory used (MB)', light_blue_format)

                filename = memory_info_after_clear_process_list[i]
                get_memory_info_time = filename.strip('meminfo_after_clear_process_|.txt')
                get_memory_info_time = get_memory_info_time.replace('_', ' ')
                get_memory_info_time = get_memory_info_time.replace('-', ':')

                with open(memory_info_dir + os.path.sep + dir_name + os.path.sep + filename, 'r') as f:
                    file = f.readlines()

                for line in file:
                    if "Free RAM:" in line:
                        line = line.strip('Free RAM (MB): ')
                        line = line.split('kB')
                        free_ram_after_cleaning_processes = float(int(line[0]) / 1000)
                    if "Used RAM:" in line:
                        line = line.strip('Used RAM (MB): ')
                        line = line.split('kB')
                        used_ram_after_cleaning_processes = float(int(line[0]) / 1000)

                worksheet.write('D' + str(round_row_num + 2), get_memory_info_time, default_cell_format)
                worksheet.write('D' + str(round_row_num + 3), used_ram_after_cleaning_processes, num_cell_format)
                worksheet.write('D' + str(round_row_num + 4), free_ram_after_cleaning_processes, num_cell_format)

                for a in range(8, 27, 2):
                    b = int(a / 2 - 4)
                    process_name = file[a].strip().split('kB: ')[1]
                    process_mem_usage = file[a].strip().split('kB: ')[0]
                    process_mem_usage = float(int(process_mem_usage) / 1000)
                    process_cell_row_num = str(15 + b + i * 17)

                    worksheet.write('C' + process_cell_row_num, process_name, process_name_cell_format)
                    worksheet.write('D' + process_cell_row_num, process_mem_usage, num_cell_format)

                start_cell_row_num = 9 + i * 17

                worksheet.merge_range('E' + str(start_cell_row_num) + ':F' + str(start_cell_row_num + 1),
                                      'Memory Interpolation', blue_format)
                worksheet.write('E' + str(start_cell_row_num + 2), 'Used RAM (MB)', light_blue_format)
                worksheet.write('E' + str(start_cell_row_num + 3), 'Free RAM (MB)', light_blue_format)
                worksheet.merge_range('E' + str(start_cell_row_num + 4) + ':F' + str(start_cell_row_num + 15),
                                      '', light_grey_format)
                worksheet.write('F' + str(start_cell_row_num + 2),
                                '=B' + str(start_cell_row_num + 2) + '-D' + str(start_cell_row_num + 2),
                                num_cell_format)
                worksheet.write('F' + str(start_cell_row_num + 3),
                                '=D' + str(start_cell_row_num + 3) + '-B' + str(start_cell_row_num + 3),
                                num_cell_format)

    workbook.close()
    print(time.ctime() + "~~ '" + result_name + "' saved.")

# resultMakerNew('..\\Result\\2017.07.25_18-07-11\\')
