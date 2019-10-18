import pymysql
import csv
import re

class base_zjx:
    def __init__(self,file,db,table):
        self.db = db
        self.cursor = None
        self.db_conn = None
        self.sqls = []
        self.file = file
        self.table = table

    def initdb(self):
        """
        从数据库获取待爬取用户身份证号码
        """
        db_conn = pymysql.connect(self.db['host'], self.db['user'], self.db['password'], self.db['db_name'])
        cursor = db_conn.cursor()
        self.cursor = cursor
        self.db_conn = db_conn

    def save_data(self):
        for sql in self.sqls:
            print('sql ==> {}'.format(sql))
            try:
                self.cursor.execute(sql)
                self.db_conn.commit()

            except Exception as e:
                print(e)

            # print(sql)


        self.sqls = []
        self.db_conn.commit()

    def __del__(self):
        self.cursor.close()
        self.db_conn.close()

class zjxcell(base_zjx):


    def run(self):
        self.initdb()
        try:
            with open(self.file, encoding='gb2312', errors='ignore') as file:
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



    def make_sql(self, result):
        sql = "SELECT Alternate5,Alternate6 from {} where Site_ID='{}'".format(self.table,result[6])
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            # print(results)
            # if len(results)!= 0:
            #     for i in results[0]:
            #         for j in i:
            #             print(j, end='')
            #     print('\n')
        except Exception as e:
            print(e)
        if len(results)!=0:    
            try:
                s6 = results[0][0]
                s7 = results[0][1]
            except e:
                print(e)
        else:
            s6 = 'NUll'
            s7 = 'NULL'
        
        s0 = result[5]
        s1 = result[11]
        s2 = result[11][:2]
        s3 = result[3]+'市'
        s4 = s3
        s5 = '3'        
        s8 = result[8]
        s9 = result[11]

        s10= result[4]

        s11= result[8]

        s12= result[9]
        s13= 'c'
        sql1 = "insert into  {}   values('{}', '{}', '{}', '{}', NULL, NULL, NULL, NULL, '{}', NULL, NULL, '{}',".format(self.table,s0,s1,s2,s3,s4,s5)
        str  =  'NULL,'
        sql2 = "'{}', '{}', NULL, NULL, NULL, NULL, NULL, '{}','{}', '{}', '{}', '{}', '{}');".format(s6,s7,s8,s9,s10,s11,s12,s13)
        sql = sql1 + str * 57 + sql2


        # print(sql)


        self.sqls.append(sql)





class zjx(base_zjx):
    def run(self):
        self.initdb()
        try:
            with open(self.file, encoding='gb2312', errors='ignore') as file:
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
        sql1 = "insert into  {}  values('{}', '{}', '{}', '{}', NULL, NULL, NULL, NULL, '{}', NULL, NULL, '{}',".format(self.table,s0,s1,s2,s3,s4,s5)
        str  =  'NULL,'
        sql2 = "'{}', '{}', NULL, NULL, NULL, NULL, NULL, '{}','{}', '{}', '{}', '{}', '{}');".format(s6,s7,s8,s9,s10,s11,s12,s13)
        sql = sql1 + str * 57 + sql2
        # print(sql)

        self.sqls.append(sql)


    

if __name__ == '__main__':
    db ={
            'host': '192.168.159.23',
            'user': 'root',
            'password': '123456',
            'db_name':  'test'  #'eprocess'
        }

    file_zjx = r'f:/prom/lt/zjx20191014.csv'
    file_cell = r'f:/prom/lt/zjxcell20191014.csv'
    tag_table = 'set_basestation_6'

    s = zjx(db=db,file=file_zjx,table=tag_table)
    s.run()
    s.save_data()
    del s

    t = zjxcell(db=db,file = file_cell,table=tag_table)
    t.run()
    t.save_data()
    del t


