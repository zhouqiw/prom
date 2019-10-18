import  pandas as pd
from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker

engine=create_engine("mysql+pymysql://root:Runsdata@2017#7v8@server02:3307/fx_data",encoding='utf-8',echo=True)

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
    print('staring...')
    df = pd.read_excel('new1.xlsx', sheet_name='w')
    base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    Session = Session_class()
    for i in df.index.values:
        s0 ,s1 = str(df.ix[i, 1]), str(df.ix[i, 9])
        if len(s0) > 64:
            s0 = s0[:64]
        if len(s1) > 64:
            s1 = s1[:64]
        if s0 !='nun':
            Session.add(user(id_num=s0))
            Session.commit()
        if s1 !='nun':
            Session.add(user(id_num=s1))
            Session.commit()


input_w()
