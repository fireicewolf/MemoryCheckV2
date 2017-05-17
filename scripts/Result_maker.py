# coding=utf-8

import os
import time
import xlsxwriter


def resultMaker(savepath):
    dumpsyslogs=savepath+'dumpsys_logs'
    
    resultName=savepath+"Test Result.xlsx"
    workbook = xlsxwriter.Workbook(resultName)
    for dirpath,dirnames,filenames in os.walk(dumpsyslogs):
        for dirname in dirnames:
            getname=dirname.split("__")

            manufacturer=getname[0]
            model=getname[1]
            deviceid=getname[2]
            buildVersion=getname[3]
            
            worksheet=workbook.add_worksheet(model+' '+deviceid)
            
            titleFormat=workbook.add_format({'font_name': 'Arial', 'font_size': 18, 'bold': True, 'bg_color': '#00B0F0',
                                             'align': 'center', 'valign': 'vcenter', 'border': 1})
            greenTitleFormat=workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                                  'valign': 'vcenter', 'border': 1, 'bg_color': '#92D050'})
            greenTitleNumFormat=workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                                     'valign': 'vcenter', 'border': 1, 'bg_color': '#92D050',
                                                     'num_format': '0.00'})
            yellowTitleFormat=workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                                   'valign': 'vcenter', 'border': 1, 'bg_color': '#FFC000',
                                                   'bold': True})
            greyTitleFormat=workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                                 'valign':'vcenter', 'border': 1, 'bg_color': '#A6A6A6'})
            defaultCellFormat=workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                                   'valign': 'vcenter', 'border': 1})
            numCellFormat=workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'align': 'center',
                                               'valign':'vcenter', 'border': 1, 'num_format': '0.00'})
            processNameCellFormat=workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'valign': 'vcenter',
                                                       'border':1})
            
            worksheet.merge_range('A1:J1', 'Memory Usage Test', titleFormat)
            worksheet.merge_range('A2:C2', 'Manufacturer', greenTitleFormat)
            worksheet.merge_range('D2:E2', manufacturer, greenTitleFormat)
            worksheet.merge_range('F2:H2', 'Model', greenTitleFormat)
            worksheet.merge_range('I2:J2', model, greenTitleFormat)
            worksheet.merge_range('A3:C3', 'Device', greenTitleFormat)
            worksheet.merge_range('D3:E3', deviceid, greenTitleFormat)
            worksheet.merge_range('F3:H3', 'Build Version', greenTitleFormat)
            worksheet.merge_range('I3:J3', buildVersion, greenTitleFormat)
            worksheet.merge_range('A4:J4', 'Before Test', yellowTitleFormat)

            meminfo_before_clear_process_list = list()
            meminfo_after_clear_process_list = list()
            for dirpath, dirnames, filenames in os.walk(dumpsyslogs+os.path.sep+dirname):
                for filename in filenames:
                    if filename.startswith('meminfo_before_test_'):
                        getmemtime = filename.strip('meminfo_before_test_|.txt')
                        getmemtime = getmemtime.replace('_',' ')
                        getmemtime = getmemtime.replace('-',':')
                        
                        with open(dumpsyslogs+os.path.sep+dirname+os.path.sep+filename, 'r') as f:
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

                        worksheet.merge_range('A5:B5', 'Test Time', greenTitleFormat)
                        worksheet.merge_range('C5:D5', getmemtime, greenTitleFormat)
                        worksheet.write('E5', 'Total RAM (MB)', greenTitleFormat)
                        worksheet.write('F5', totalRAM, greenTitleNumFormat)
                        worksheet.write('G5', 'Free RAM (MB)', greenTitleFormat)
                        worksheet.write('H5', freeRAM, greenTitleNumFormat)
                        worksheet.write('I5', 'Used RAM (MB)', greenTitleFormat)
                        worksheet.write('J5', usedRAM, greenTitleNumFormat)
                        worksheet.merge_range('A6:J6', 'Before Test', yellowTitleFormat)

                    if filename.startswith('meminfo_before_clear_process_'):
                        meminfo_before_clear_process_list.append(filename)

                    if filename.startswith('meminfo_after_clear_process_'):
                        meminfo_after_clear_process_list.append(filename)

            for i in range(len(meminfo_before_clear_process_list)):
                filename = meminfo_before_clear_process_list[i]
                getmemtime = filename.strip('meminfo_before_clear_process_|.txt')
                getmemtime = getmemtime.replace('_', ' ')
                getmemtime = getmemtime.replace('-', ':')
                 
                with open(dumpsyslogs+os.path.sep+dirname+os.path.sep+filename, 'r') as f:
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

                titleRowNum = str(7+i*6)
                cellRowStartNum = str(8+i*6)
                cellRowEndNum = str(12+i*6)
                
                worksheet.write('A'+titleRowNum, 'Before clearing process', greyTitleFormat)
                worksheet.merge_range('A'+cellRowStartNum+':A'+cellRowEndNum, getmemtime, defaultCellFormat)
                 
                worksheet.write('B'+titleRowNum, 'Top 5 Process', greyTitleFormat)
                worksheet.write('C'+titleRowNum, 'Memory Usage', greyTitleFormat)
                
                for a in range(8, 17, 2):
                    b = int(a/2-4)
                    processName = file[a].strip().split('kB: ')[1]
                    processMemUsage = file[a].strip().split('kB: ')[0]
                    processMemUsage = float(int(processMemUsage)/1000)
                    processCellRowNum = str(8+b+i*6)
                    
                    worksheet.write('B'+processCellRowNum, processName, processNameCellFormat)
                    worksheet.write('C'+processCellRowNum, processMemUsage, numCellFormat)
                 
                worksheet.write('D'+titleRowNum, 'Free RAM (MB)', greyTitleFormat)
                worksheet.merge_range('D'+cellRowStartNum+':D'+cellRowEndNum, freeRAM, numCellFormat)
                 
                worksheet.write('E'+titleRowNum, 'Used RAM (MB)', greyTitleFormat)
                worksheet.merge_range('E'+cellRowStartNum+':E'+cellRowEndNum, usedRAM, numCellFormat)
                
            for i in range(len(meminfo_after_clear_process_list)):
                filename = meminfo_after_clear_process_list[i]
                getmemtime = filename.strip('meminfo_after_clear_process_|.txt')
                getmemtime = getmemtime.replace('_', ' ')
                getmemtime = getmemtime.replace('-', ':')
                 
                with open(dumpsyslogs+os.path.sep+dirname+os.path.sep+filename, 'r') as f:
                    file = f.readlines()
                     
                for line in file:
                    if "Free RAM:" in line:
                        line = line.strip('Free RAM: ')
                        line = line.split('kB')
                        freeRAM = float(int(line[0])/1000)
                    if "Used RAM:" in line:
                        line = line.strip('Used RAM: ')
                        line = line.split('kB')
                        usedRAM = float(int(line[0])/1000)

                titleRowNum = str(7+i*6)
                cellRowStartNum = str(8+i*6)
                cellRowEndNum = str(12+i*6)
                
                worksheet.write('F'+titleRowNum,'After clearing process', greyTitleFormat)
                worksheet.merge_range('F'+cellRowStartNum+':F'+cellRowEndNum, getmemtime, defaultCellFormat)
                 
                worksheet.write('G'+titleRowNum, 'Top 5 Process', greyTitleFormat)
                worksheet.write('H'+titleRowNum, 'Memory Usage', greyTitleFormat)
                
                for a in range(8, 17, 2):
                    b = int(a/2-4)
                    processName = file[a].strip().split(': ')[1]
                    processMemUsage = file[a].strip().split('kB: ')[0]
                    processMemUsage = float(int(processMemUsage)/1000)
                    processCellRowNum = str(8+b+i*6)
                    
                    worksheet.write('G'+processCellRowNum, processName, processNameCellFormat)
                    worksheet.write('H'+processCellRowNum, processMemUsage, numCellFormat)
                 
                worksheet.write('I'+titleRowNum, 'Free RAM (MB)', greyTitleFormat)
                worksheet.merge_range('I'+cellRowStartNum+':I'+cellRowEndNum, freeRAM, numCellFormat)
                 
                worksheet.write('J'+titleRowNum, 'Used RAM (MB)', greyTitleFormat)
                worksheet.merge_range('J'+cellRowStartNum+':J'+cellRowEndNum, usedRAM, numCellFormat)
                
    workbook.close()
    print(time.ctime()+"~~ Test result saved.")