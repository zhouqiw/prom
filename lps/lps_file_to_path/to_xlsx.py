# -*- coding: UTF-8 -*-
import xlsxwriter
import datetime
import time


def w_file(file,data):
    startTime1 = time.time()
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()
    title = ['身份证号','姓名', '性别','民族','出生地','出生日期','户口类别','常住户口地地址','通讯地址', '邮政编码','联系电话','人员状态','文化程度','个人编号','单位编号','行政区划','参保状态','最后缴费','待遇开始'	]
    worksheet.write_row('A1', title)
    for i in range(0, len(data)):
        worksheet.write_row(i+1, 0, data[i])
    workbook.close()

file = 'd:\kami1.xlsx'
data = [['ni', 'hao'],['hi', 'hsing']]

w_file(file,data)
