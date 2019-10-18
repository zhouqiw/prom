import pymysql
import csv
import re
class linatong:
    def __init__(self):
        self.db = {
            'host': '192.168.159.23',
            'user': 'root',
            'password': '123456',
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
            with open(r'f:/prom/联通/zjx20191010.csv', encoding='gb2312', errors='ignore') as file:
                reader = csv.DictReader(file)
                # print(reader.fieldnames)
                s = [i for i in reader.fieldnames if i != '']
                # s=s.remove(7)
                del s[7]
                del s[7]
                s.insert(5, '')
                # print(type(s))
                # print(s)

                for row in reader:
                    l = []
                    for k, v in row.items():
                        # print(v,end=' ')
                        l.append(v)

                    # print(l)

                    # print(len(l))
                    # if len(l) != 18:
                        # print(l)
                    self.make_sql(l)
                self.make_sql(s)
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
        s0 = result[8]
        s1 = result[17]
        s2 = result[2]
        s3 = result[3]+'市'
        s4 = s3
        s5 = result[10]

        s6 = result[7]
        s7 = result[6]
        # print(result)
        # print(s6,s7)

        s8 = result[9]
        s9 = result[16]
        s10= result[4]
        s11= result[13]
        s12= result[14]
        s13= result[15]
        sql1 = "insert into  set_basestation  values('{}', '{}', '{}', '{}', NULL, NULL, NULL, NULL, '{}', NULL, NULL, '{}',".format(s0,s1,s2,s3,s4,s5)
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


