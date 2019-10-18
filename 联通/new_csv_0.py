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
                        self.make_sql(p)

                    if len(l) == 12:
                        self.make_sql(l)
        except Exception as e:
            print(e)

    def save_data(self):
        for sql in self.sqls:
            # print('sql ==> {}'.format(sql))
            try:
                self.cursor.execute(sql)
                self.db_conn.commit()

            except Exception as e:
                print(e)

            # print(sql)


        self.sqls = []
        self.db_conn.commit()

    def make_sql(self, result):
        s0 = result[5]
        s1 = result[11]
        s2 = result[11][:2]
        s3 = result[3]+'市'
        s4 = s3

        s5 = '3'

        s6 = 'NULL'
        s7 = 'NULL'

        s8 = result[8]
        s9 = result[11]

        s10= result[4]

        s11= result[8]

        s12= result[9]
        s13= 'c'
        sql1 = "insert into  set_basestation_1   values('{}', '{}', '{}', '{}', NULL, NULL, NULL, NULL, '{}', NULL, NULL, '{}',".format(s0,s1,s2,s3,s4,s5)
        str  =  'NULL,'
        sql2 = "'{}', '{}', NULL, NULL, NULL, NULL, NULL, '{}','{}', '{}', '{}', '{}', '{}');".format(s6,s7,s8,s9,s10,s11,s12,s13)
        sql = sql1 + str * 57 + sql2


        # print(sql)


        self.sqls.append(sql)



    def __del__(self):
        self.cursor.close()
        self.db_conn.close()



if __name__ == '__main__':

    s = linatong()
    s.run()
    s.save_data()
    del s


