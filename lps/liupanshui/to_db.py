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
class users(base):
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


# def input_w():
#     print('staring...')
#     df = pd.read_excel(r'C:\Users\zhouweiqi\Desktop\1\2\new1.xlsx', sheet_name='w')
#     base.metadata.create_all(engine)
#     Session_class = sessionmaker(bind=engine)
#     Session = Session_class()
#     for i in df.index.values:
#         s0 ,s1 = str(df.ix[i, 1]), str(df.ix[i, 9])
#         if len(s0) > 64:
#             s0 = s0[:64]
#         if len(s1) > 64:
#             s1 = s1[:64]
#         if s0 !='nun':
#             Session.add(user(id_num=s0))
#             Session.commit()
#         if s1 !='nun':
#             Session.add(user(id_num=s1))
#             Session.commit()
#
#
#
# # input_w()

df = pd.read_excel('new0.xlsx', sheet_name='qb1')
base.metadata.create_all(engine)
Session_class = sessionmaker(bind=engine)
Session = Session_class()
print(Session.query(data_q).count())
tag =Session.query(data_q).count() - 1012741
print(tag)
def to_data_q(s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16):

    obj=(data_q(id_num=s0, name=s1, int_1=s2, int_2=s3,addr_1=s4, data_b=s5, int_3=s6,addr_pjs=s7, addr_2=s8, int_4=s9,ph_or_te=s10, int_5=s11,int_6=s12,int_7=s13, int_8=s14, int_9=s15, int_10=s16))
    Session.add(obj)
    Session.commit()




#df = pd.read_excel('new0.xlsx', sheet_name='qb2')
print(df.index.values)
# df = pd.read_excel(r'C:\Users\zhouweiqi\Desktop\1\2\new1.xlsx', sheet_name='qb1')
print('staring')
for i in df.index.values:
    #print(str(df.ix[i,2]))
    if tag < i:
        s0 = str(df.ix[i, 1])
        s1 = str(df.ix[i, 2])
        s2 = str(df.ix[i, 3])
        s3 = str(df.ix[i, 4])
        s4 = str(df.ix[i, 5])
        s5 = str(df.ix[i, 6])
        s6 = str(df.ix[i, 7])
        s7 = str(df.ix[i, 8])
        s8 = str(df.ix[i, 9])
        s9 = (str(df.ix[i, 10]))[:-2]
        s10 = str(df.ix[i, 11])
        s11 = str(df.ix[i, 12])
        s12 = str(df.ix[i, 14])
        s13 = str(df.ix[i, 15])
        s14 = str(df.ix[i, 16])
        s15 = str(df.ix[i, 17])
        s16 = str(df.ix[i, 19])
        for j in range(19):
            if len(s8) > 32:
                s8 = s8[:32]
            if len(s5) >32:
                s5 = s5[:32]
            if len(s7) >32:
                s7 = s7[:32]
        to_data_q(s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16)



