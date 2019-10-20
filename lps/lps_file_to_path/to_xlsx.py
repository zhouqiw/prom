# -*- coding: UTF-8 -*-

import datetime
import time
import os
import xlsxwriter
from   xlrd         import open_workbook
from   xlutils.copy import copy


def jishi(a_func):
    def wrapTheFunction():
        startTime = time.time()
        a_func()
        print('use time is {}'.format(time.time() - startTime))
    return wrapTheFunction


@jishi
def w_file(file,data):
    if os.path.exists(file):
        rexcel = open_workbook(file)
        rows = rexcel.sheets()[0].nrows
        excel = copy(rexcel)
        table = excel.get_sheet(0)
        row = rows
        print(row)
        # table.write_row(row,data)
        for i in range(len(data)):
            table.write(row, i, data[i])

        excel.save(file)
    else:


        workbook = xlsxwriter.Workbook(file)
        worksheet = workbook.add_worksheet()
        title = ['身份证号','姓名', '性别','民族','出生地','出生日期','户口类别','常住户口地地址','通讯地址', '邮政编码','联系电话','人员状态','文化程度','个人编号','单位编号','行政区划','参保状态','最后缴费','待遇开始'	]
        print(type(title[0]))
        worksheet.write_row('A1', title)

        worksheet.write_row('A2',data)
        workbook.close()














# file = 'd:\kami1.xlsx'
# data = [['ni', 'hao'],['hi', 'hsing']]
#
# w_file(file,data)
