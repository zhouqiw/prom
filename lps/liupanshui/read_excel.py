# -*-coding:utf-8-*-
# import  pandas as pd
# df = pd.read_excel(r'C:\Users\zhouweiqi\Desktop\1\2\12345.xlsx',sheet_name='Sheet2')
# # data=df.head()
# # print("获取到所有的值:\n{0}".format(data))#格式化输出
# print("输出列标题",df.columns.values)
# for i in df.index.values:
#     df

import  pandas as pd
from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker

engine=create_engine("mysql+pymysql://root:Runsdata@2017#7v8@localhost:3307/fx_data",encoding='utf-8',echo=True)

base=declarative_base()
class user(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    id_num = Column(String(64))

class data_q(base):
    __tablename__ = 'data_q'
    id = Column(Integer, primary_key=True)
    id_num = Column(String(64))
    name = Column(String(32))
    int_1=  Column(String(16))
    int_2 = Column(String(16))
    addr_1 = Column(String(32))
    data_b= Column(String(32))
    int_3 = Column(String(32))
    addr_pjs = Column(String(32))
    addr_2 = Column(String(32))
    int_4 = Column(String(32))
    ph_or_te =Column(String(64))
    int_5 = Column(String(16))
    int_6 = Column(String(32))
    int_7 = Column(String(32))
    int_8 = Column(String(32))
    int_9 = Column(String(16))
    int_10 = Column(String(32))


def input_w():
    df = pd.read_excel(r'C:\Users\zhouweiqi\Desktop\1\2\new.xlsx', sheet_name='w')
    base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    Session = Session_class()
    for i in df.index.values:
        print(df.ix[i, 1], )
        user_1 = user(id_num=df.ix[i, 1])
        print(df.ix[i, 9])
        user_2 = user(id_num=df.ix[i, 9])
        Session.add(user_1)
        Session.add(user_2)
        Session.commit()


# input_w()

df = pd.read_excel(r'C:\Users\zhouweiqi\Desktop\1\2\new0.xlsx', sheet_name='qb1')
base.metadata.create_all(engine)
Session_class = sessionmaker(bind=engine)
Session = Session_class()
print(Session.query(data_q).count())
tag =Session.query(data_q).count()
for i in df.index.values:
    if tag < i:

        # print(df.ix[i, 1],df.ix[i, 2], df.ix[i, 3],df.ix[i, 4],df.ix[i, 5],df.ix[i, 6],df.ix[i, 7],df.ix[i, 8],df.ix[i, 9],(str(df.ix[i, 10]))[:-2],df.ix[i, 11],df.ix[i, 12],df.ix[i, 14],df.ix[i, 15],df.ix[i, 16],df.ix[i, 17],df.ix[i, 19])
        data_obj = data_q(id_num=str(df.ix[i, 1]), name=str(df.ix[i, 2]), int_1=str(df.ix[i, 3]), int_2=str(df.ix[i, 4]), addr_1=str(df.ix[i, 5]), data_b=str(df.ix[i, 6]),int_3=str(df.ix[i, 7]), addr_pjs=str(df.ix[i, 8]), addr_2=str(df.ix[i, 9]), int_4=(str(df.ix[i, 10]))[:-2], ph_or_te=str(df.ix[i,11]), int_5=str(df.ix[i, 12]),int_6=str(df.ix[i, 14]), int_7=str(df.ix[i, 15]), int_8=str(df.ix[i, 16]), int_9=str(df.ix[i, 17]), int_10=str(df.ix[i, 19]))
        Session.add(data_obj)
        Session.commit()
