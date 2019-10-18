import pymysql
import csv
from multiprocessing import Queue,Process
import time
import pymysql

conn = pymysql.connect(host='134.98.184.112', user='root',password='Gxlt1234!@#$',database='test',charset='utf8')
cursor = conn.cursor()

def make_sql(q, result):
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
    sql1 = "insert into  set_basestation_2   values('{}', '{}', '{}', '{}', NULL, NULL, NULL, NULL, '{}', NULL, NULL, '{}',".format(s0,s1,s2,s3,s4,s5)
    str  =  'NULL,'
    sql2 = "'{}', '{}', NULL, NULL, NULL, NULL, NULL, '{}','{}', '{}', '{}', '{}', '{}');".format(s6,s7,s8,s9,s10,s11,s12,s13)
    sql = sql1 + str * 57 + sql2
    q.put(sql)
def producer(q):
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
                    make_sql(q,p)

                if len(l) == 12:
                    make_sql(q,l)
    except Exception as e:
        print(e)

def consumer(q):
    while True:
        res=q.get()
        try:
            cursor.execute(res)
            conn.commit()

        except Exception as e:
            print(e)

        # print('sql --> %s'%(res))



if __name__ == '__main__':
    q = Queue()  # 一个队列

    p1 = Process(target=producer, args=( q,))
    c1 = Process(target=consumer, args=( q,))
    c2 = Process(target=consumer, args=(q,))
    c3 = Process(target=consumer, args=(q,))
    c4 = Process(target=consumer, args=(q,))
    c5 = Process(target=consumer, args=(q,))
    c6 = Process(target=consumer, args=(q,))

    p1.start()
    c1.start()
    c2.start()
    c3.start()
    c4.start()
    c5.start()
    c6.start()


