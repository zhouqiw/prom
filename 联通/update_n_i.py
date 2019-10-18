import pymysql
import csv
import re
class linatong:
    def __init__(self):
        self.db = {
            'host': '134.98.184.112',
            'user': 'root',
            'password': 'Gxlt1234!@#$',
            'db_name':  'test'  #'eprocess'
        }
        self.cursor = None
        self.db_conn = None
        self.sqls = []

    def initdb(self):
        """
        从数据库获取待爬取用户身份证号码
        """
        db_conn = pymysql.connect(self.db['host'], self.db['user'], self.db['password'], self.db['db_name'])
        cursor = db_conn.cursor()
        self.cursor = cursor
        self.db_conn = db_conn

    def run(self):
        self.initdb()

        try:
            with open(r'f:/prom/联通/zjxcell20191010.csv', encoding='gb2312', errors='ignore') as file:
                reader = csv.DictReader(file)
                print(reader.fieldnames)
                s = [i for i in reader.fieldnames if i != '']
                print(type(s))
                print(s)
                for row in reader:
                    k = ''
                    l = [v for k, v in row.items()]
                    if len(l) > 12:
                        # print(l[:11])
                        for i in l[11:]:
                            # print(i)
                            if type(i) == str:
                                k = k + '-' + i
                            elif type(i) == list:
                                for j in i:
                                    k = k + '-' + j
                        # print(k)
                        p = l[:11]
                        p.insert(11, k)
                        # print(p)
                        self. next_make(p)

                    if len(l) == 12:
                        self. next_make(l)
        except Exception as e:
            print(e)



    def next_make(self,l):
        sql = "SELECT Alternate5,Alternate6 from set_basestation_1 where Site_ID={}".format(l[6])
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            print(results)
            if len(results)!= 0:
                for i in results[0]:
                    for j in i:
                        print(j, end='')
                print('\n')
        except Exception as e:
            print(e)
        try:
            if len(results)!= 0:
                sql_update = "update set_basestation_1 set Alternate5={},Alternate6={} where Site_ID ={}".format(results[0][0],results[0][1],l[0])
                self.cursor.execute(sql)
        except Exception as e:
            print(e)







    def __del__(self):
        self.cursor.close()
        self.db_conn.close()



if __name__ == '__main__':

    s = linatong()
    s.run()
    s.save_data()
    del s


