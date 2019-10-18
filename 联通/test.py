# -*-coding:utf-8-*-

import pymysql
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
            c = open(r'f:/prom/联通/zjx20190929.txt', 'r').readlines()
            s = 0
            s19, s16, s17, s18 = 0, 0, 0, 0
            for item in c:
                # print(item)
                str_0 = item.replace('***************', '*').replace('****', '*').replace('***','*').replace('**','*')
                # print(str_0)
                l = str_0.split('*')


                if len(l) == 18 :
                    # s18 = s18+1
                    # if l[7]=='15555880927':
                    #     print(l[13])
                    # print('--->18',l)
                    # self.make_sql(l)
                    pass
                elif len(l) ==17:
                    s17= s17+1
                    # print('--->17',l)
                    pass
                elif len(l) <=16:
                    s16= s16+1
                    print('--->{}'.format(len(l)),l)
                    # self.make_sql(l)
                    pass

                elif len(l) >18:
                    s15 = s19+1
                    # print('--->{}'.format(len(l)), l)
                    # del l[14]
                    # print('--->{}'.format(len(l)),l)
                    pass
                else:
                    s = s + 1
                    # print(len(l))
                    # print(l)
            print('s15=',s19,'   s16=',s16,'    s17=',s17,'     s18=',s18,'    其他=',s)
        except Exception as e:
            print('exception ==> {}'.format(e))

    def save_data(self):
        for sql in self.sqls:
            print('sql ==> {}'.format(sql))
            try:
                self.cursor.execute(sql)
            except Exception as e:
                print('error ==> {}'.format(e))
            # self.cursor.execute(sql)


        self.sqls = []
        self.db_conn.commit()

    def make_sql(self, result):
        s0 = result[10]
        s1 = result[5]
        s2 = s1[:3].replace('-','').replace('-','')
        s3 = result[3]+'市'
        s4 = s3
        s5 = result[12]
        s6 = result[7]
        s7 = result[8]
        s8 = result[11]
        s9 = ''.join(re.findall('[\u4e00-\u9fa5]',s1))
        s10= result[4]
        s11= result[13]
        s12= result[14]
        s13= result[15]
        sql1 = "insert into  set_basestation0   values('{}', '{}', '{}', '{}', NULL, NULL, NULL, NULL, '{}', NULL, NULL, '{}',".format(s0,s1,s2,s3,s4,s5)
        str  =  'NULL,'
        sql2 = "'{}', '{}', NULL, NULL, NULL, NULL, NULL, '{}','{}', '{}', '{}', '{}', '{}');".format(s6,s7,s8,s9,s10,s11,s12,s13)
        sql = sql1 + str * 57 + sql2
        print(sql)

        self.sqls.append(sql)


    def __del__(self):
        self.cursor.close()
        self.db_conn.close()



if __name__ == '__main__':

    s = linatong()
    s.run()
    # s.save_data()
    del s

    #     0         1     2      3    4                            5                           6       7         8       9                         10       11   12   13  14  15
    # 2019-09-29* 移动网*NODEB *滁州*华为****CUZ-天长宿扬高速1（天长平安虎山）(工程站.8）-U_B类*张继兵*15605502483*张继兵*15605502483***************-1866089649*WNMS*2***OTHER*3G*B*
    # ['2019-09-29', '移动网', 'NODEB', '安庆', '华为', 'AQ-太湖百里柳青自有-U', '杨友旺', '13155561220', '杨友旺', '13155561220',     '1235533228', 'WNMS', '1', 'AQ01317', '乡郊', 'OTHER', '3G', 'A', '太湖百里柳青自有\n']
    # ['2019-09-29', '移动网', 'ENODEB', '滁州', '华为', 'CUZ-天长秦栏政府-F_A类', '张继兵', '15605502483', '张继兵', '15605502483', '802422868', 'WNMS', '1', 'CUZ31459', 'OTHER', '4G', 'A', '天长市秦栏镇秦栏镇街道\n']
    # ['2019-09-29', '移动网', 'NODEB', '滁州', '华为', 'CUZ-天长宿扬高速1（天长平安虎山）(工程站.8）-U_B类', '张继兵', '15605502483', '张继兵', '15605502483', '-1866089649', 'WNMS', '2', 'OTHER', '3G', 'B', '']
    # ['2019-09-29', '移动网', 'ENODEB', '阜阳', '中兴', 'FY-界首市-四季花城-TYGC(4G)-界首新联通-F',          '肖海龙', '18655869905', '肖海龙', '18655869905', '-838826169', 'WNMS', '3', 'OTHER', '4G', 'C', 'unknown\n']
    # ['2019-09-29', '移动网', 'ENODEB', '蚌埠', '中兴', 'BB-龙子湖区电子学院西南-UL-F',                        '熊鹰', '18655292963', '熊鹰', '18655292963',  '-1250310830', 'WNMS', '2', 'OTHER', '4G', 'B', 'unknown\n']
    # ('-1836366898', 'HF-置地广场D座-W', 'HF', '合肥市', NULL, NULL, NULL, NULL, '合肥市', NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
    # NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
    # NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '18655150449', '童飞', NULL, NULL, NULL, NULL, NULL, 'HF7797', '置地广场D座', '中兴', 'OTHER', '3G', 'A');
