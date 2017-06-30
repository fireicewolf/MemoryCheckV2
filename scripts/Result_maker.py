# coding=utf-8

import os
import time
import xlsxwriter


def resultMaker(save_path):
    memory_info_dir = save_path + 'dumpsys_logs'
    result_name = save_path + "Test Result.xlsx"

    print(time.ctime()+"~~ Saving test result: " + result_name)

    workbook = xlsxwriter.Workbook(result_name)
    for dirpath, dirnames, filenames in os.walk(memory_info_dir):
        for dirname in dirnames:
            getname = dirname.split("__")

            manufacturer = getname[0]
            model = getname[1]
            device_id = getname[2]
            build_version = getname[3]
            
            worksheet = workbook.add_worksheet(model+' '+device_id)
            
            title_format = workbook.add_format({'font_name': 'Arial', 'font_size': 18, 'bold': True,
                                                'bg_color': '#00B0F0', 'align': 'center', 'valign': 'vcenter',
                                                'border': 1})

            green_title_format = workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                                      'valign': 'vcenter', 'border': 1, 'bg_color': '#92D050'})

            green_title_num_format = workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                                          'valign': 'vcenter', 'border': 1, 'bg_color': '#92D050',
                                                          'num_format': '0.00'})

            yellow_title_format = workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                                       'valign': 'vcenter', 'border': 1, 'bg_color': '#FFC000',
                                                       'bold': True})

            grey_title_format = workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                                     'valign': 'vcenter', 'border': 1, 'bg_color': '#A6A6A6'})

            default_cell_format = workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                                       'valign': 'vcenter', 'border': 1})

            num_cell_format = workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                                   'valign': 'vcenter', 'border': 1, 'num_format': '0.00'})

            process_name_cell_format = workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'valign': 'vcenter',
                                                            'border': 1})
            
            worksheet.merge_range('A1:J1', 'Memory Usage Test', title_format)
            worksheet.merge_range('A2:C2', 'Manufacturer', green_title_format)
            worksheet.merge_range('D2:E2', manufacturer, green_title_format)
            worksheet.merge_range('F2:H2', 'Model', green_title_format)
            worksheet.merge_range('I2:J2', model, green_title_format)
            worksheet.merge_range('A3:C3', 'Device', green_title_format)
            worksheet.merge_range('D3:E3', device_id, green_title_format)
            worksheet.merge_range('F3:H3', 'Build Version', green_title_format)
            worksheet.merge_range('I3:J3', build_version, green_title_format)
            worksheet.merge_range('A4:J4', 'Before Test', yellow_title_format)

            memory_info_before_clear_process_list = list()
            memory_info_after_clear_process_list = list()
            for resultdirpath, resultdirnames, resultfilenames in os.walk(memory_info_dir+os.path.sep+dirname):
                for resultfilename in resultfilenames:
                    if resultfilename.startswith('meminfo_before_test_'):
                        get_memory_info_time = resultfilename.strip('meminfo_before_test_|.txt')
                        get_memory_info_time = get_memory_info_time.replace('_', ' ')
                        get_memory_info_time = get_memory_info_time.replace('-', ':')
                        
                        with open(memory_info_dir+os.path.sep+dirname+os.path.sep+resultfilename, 'r') as f:
                            file = f.readlines()
                            
                        for line in file:
                            if "Total RAM:" in line:
                                line = line.strip('Total RAM: ')
                                line = line.split('kB')
                                totalRAM = float(int(line[0])/1000)
                            if "Free RAM:" in line:
                                line = line.strip('Free RAM: ')
                                line = line.split('kB')
                                freeRAM = float(int(line[0])/1000)
                            if "Used RAM:" in line:
                                line = line.strip('Used RAM: ')
                                line = line.split('kB')
                                usedRAM = float(int(line[0])/1000)
                            # else:
                            #     totalRAM = "null"
                            #     freeRAM = "null"
                            #     usedRAM = "null"

                        worksheet.merge_range('A5:B5', 'Test Time', green_title_format)
                        worksheet.merge_range('C5:D5', get_memory_info_time, green_title_format)
                        worksheet.write('E5', 'Total RAM (MB)', green_title_format)
                        worksheet.write('F5', totalRAM, green_title_num_format)
                        worksheet.write('G5', 'Free RAM (MB)', green_title_format)
                        worksheet.write('H5', freeRAM, green_title_num_format)
                        worksheet.write('I5', 'Used RAM (MB)', green_title_format)
                        worksheet.write('J5', usedRAM, green_title_num_format)
                        worksheet.merge_range('A6:J6', 'Test Result', yellow_title_format)

                    if resultfilename.startswith('meminfo_before_clear_process_'):
                        memory_info_before_clear_process_list.append(resultfilename)

                    if resultfilename.startswith('meminfo_after_clear_process_'):
                        memory_info_after_clear_process_list.append(resultfilename)

            for i in range(len(memory_info_before_clear_process_list)):
                filename = memory_info_before_clear_process_list[i]
                get_memory_info_time = filename.strip('meminfo_before_clear_process_|.txt')
                get_memory_info_time = get_memory_info_time.replace('_', ' ')
                get_memory_info_time = get_memory_info_time.replace('-', ':')
                 
                with open(memory_info_dir+os.path.sep+dirname+os.path.sep+filename, 'r') as f:
                    file = f.readlines()
                     
                for line in file:
                    if "Free RAM:" in line:
                        line = line.strip('Free RAM (MB): ')
                        line = line.split('kB')
                        freeRAM = float(int(line[0])/1000)
                    if "Used RAM:" in line:
                        line = line.strip('Used RAM (MB): ')
                        line = line.split('kB')
                        usedRAM = float(int(line[0])/1000)

                title_row_num = str(7+i*6)
                cell_row_start_num = str(8+i*6)
                cell_row_end_num = str(12+i*6)
                
                worksheet.write('A'+title_row_num, 'Before clearing process', grey_title_format)
                worksheet.merge_range('A'+cell_row_start_num+':A'+cell_row_end_num,
                                      get_memory_info_time, default_cell_format)
                 
                worksheet.write('B'+title_row_num, 'Top 5 Process', grey_title_format)
                worksheet.write('C'+title_row_num, 'Memory Usage (MB)', grey_title_format)
                
                for a in range(8, 17, 2):
                    b = int(a/2-4)
                    process_name = file[a].strip().split('kB: ')[1]
                    process_mem_usage = file[a].strip().split('kB: ')[0]
                    process_mem_usage = float(int(process_mem_usage) / 1000)
                    process_cell_row_num = str(8 + b + i * 6)
                    
                    worksheet.write('B' + process_cell_row_num, process_name, process_name_cell_format)
                    worksheet.write('C' + process_cell_row_num, process_mem_usage, num_cell_format)
                 
                worksheet.write('D' + title_row_num, 'Free RAM (MB)', grey_title_format)
                worksheet.merge_range('D' + cell_row_start_num+':D'+cell_row_end_num, freeRAM, num_cell_format)
                 
                worksheet.write('E' + title_row_num, 'Used RAM (MB)', grey_title_format)
                worksheet.merge_range('E' + cell_row_start_num+':E'+cell_row_end_num, usedRAM, num_cell_format)
                
            for i in range(len(memory_info_after_clear_process_list)):
                filename = memory_info_after_clear_process_list[i]
                get_memory_info_time = filename.strip('meminfo_after_clear_process_|.txt')
                get_memory_info_time = get_memory_info_time.replace('_', ' ')
                get_memory_info_time = get_memory_info_time.replace('-', ':')
                 
                with open(memory_info_dir+os.path.sep+dirname+os.path.sep+filename, 'r') as f:
                    file = f.readlines()
                     
                for line in file:
                    if "Free RAM:" in line:
                        line = line.strip('Free RAM: ')
                        line = line.split('kB')
                        freeRAM = float(int(line[0]) / 1000)
                    if "Used RAM:" in line:
                        line = line.strip('Used RAM: ')
                        line = line.split('kB')
                        usedRAM = float(int(line[0]) / 1000)

                title_row_num = str(7 + i * 6)
                cell_row_start_num = str(8 + i * 6)
                cell_row_end_num = str(12 + i * 6)
                
                worksheet.write('F' + title_row_num, 'After clearing process', grey_title_format)
                worksheet.merge_range('F' + cell_row_start_num + ':F' + cell_row_end_num,
                                      get_memory_info_time, default_cell_format)
                 
                worksheet.write('G' + title_row_num, 'Top 5 Process', grey_title_format)
                worksheet.write('H' + title_row_num, 'Memory Usage (MB)', grey_title_format)
                
                for a in range(8, 17, 2):
                    b = int(a/2-4)
                    process_name = file[a].strip().split(': ')[1]
                    process_mem_usage = file[a].strip().split('kB: ')[0]
                    process_mem_usage = float(int(process_mem_usage)/1000)
                    process_cell_row_num = str(8 + b + i * 6)
                    
                    worksheet.write('G' + process_cell_row_num, process_name, process_name_cell_format)
                    worksheet.write('H' + process_cell_row_num, process_mem_usage, num_cell_format)
                 
                worksheet.write('I' + title_row_num, 'Free RAM (MB)', grey_title_format)
                worksheet.merge_range('I' + cell_row_start_num+':I' + cell_row_end_num, freeRAM, num_cell_format)
                 
                worksheet.write('J' + title_row_num, 'Used RAM (MB)', grey_title_format)
                worksheet.merge_range('J' + cell_row_start_num+':J' + cell_row_end_num, usedRAM, num_cell_format)

            worksheet.merge_range('A' + str(int(cell_row_end_num) + 1) + ':C' + str(int(cell_row_end_num) + 2),
                                  'Before clearing process', grey_title_format)
            worksheet.write('D' + str(int(cell_row_end_num) + 1), 'Average Free RAM (MB)', grey_title_format)
            worksheet.write('E' + str(int(cell_row_end_num) + 1), 'Average Used RAM (MB)', grey_title_format)

            worksheet.write('D' + str(int(cell_row_end_num) + 2), '=AVERAGE(D8:D' + str(cell_row_start_num) + ')',
                            default_cell_format)
            worksheet.write('E' + str(int(cell_row_end_num) + 2), '=AVERAGE(E8:E' + str(cell_row_start_num) + ')',
                            default_cell_format)

            worksheet.merge_range('F' + str(int(cell_row_end_num) + 1) + ':H' + str(int(cell_row_end_num) + 2),
                                  'After clearing process', grey_title_format)
            worksheet.write('I' + str(int(cell_row_end_num) + 1), 'Average Free RAM (MB)', grey_title_format)
            worksheet.write('J' + str(int(cell_row_end_num) + 1), 'Average Used RAM (MB)', grey_title_format)

            worksheet.write('I' + str(int(cell_row_end_num) + 2), '=AVERAGE(I8:I' + str(cell_row_start_num) + ')',
                            default_cell_format)
            worksheet.write('J' + str(int(cell_row_end_num) + 2), '=AVERAGE(J8:J' + str(cell_row_start_num) + ')',
                            default_cell_format)

    workbook.close()
    print(time.ctime()+"~~ '" + result_name + "' saved.")

# resultMaker('..\\Result\\2017.06.30_17-16-13\\')
