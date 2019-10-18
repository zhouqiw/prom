import  pandas as pd
from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker

# engine=create_engine("mysql+pymysql://root:Runsdata@2017#7v8@server02:3307/fx_data",encoding='utf-8',echo=True)
engine=create_engine("mysql+pymysql://root:Runsdata@2017#7v8@localhost:3307/fx_data",encoding='utf-8',echo=False)
base=declarative_base()


class user_zg(base):
    __tablename__ = 'user_zg'
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
    int_11 = Column(String(16))


class user_zg(base):
    __tablename__ = 'user_jm'
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
    int_11 = Column(String(16))

class dwxx(base):
    __tablename__ = 'dwxx'
    id = Column(Integer, primary_key=True)
    id_qy = Column(String(64))
    name_qy  =  Column(String(32))
    type  =  Column(String(16))
    bh    =  Column(String(16))
    name_fzr =Column(String(16))
    phone  = Column(String(32))
    bhs    = Column(String(32))


base.metadata.create_all(engine)
Session_class = sessionmaker(bind=engine)
Session = Session_class()
# print(Session.query(user_zg).count())
# tag =Session.query(user_zg).count()
tag =0
# print(tag)

def to_data_q(s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17):

    obj=(user_zg(id_num=s0, name=s1, int_1=s2, int_2=s3,addr_1=s4, data_b=s5, int_3=s6,addr_pjs=s7, addr_2=s8, int_4=s9,ph_or_te=s10, int_5=s11,int_6=s12,int_7=s13, int_8=s14, int_9=s15, int_10=s16, int_11=s17))
    Session.add(obj)
    Session.commit()


def inputs():
    df = pd.read_excel(r'C:\Users\zhouweiqi\Desktop\1\2\zhikashuju.xlsx', sheet_name='zhigong')
    print(df.index.values)
    print('staring')
    for i in df.index.values:
        print(str(df.ix[i, 2]))
        if tag < i:
            s0 = str(df.ix[i, 0])
            s1 = str(df.ix[i, 1])
            s2 = str(df.ix[i, 2])
            s3 = str(df.ix[i, 3])
            s4 = str(df.ix[i, 4])
            s5 = str(df.ix[i, 5])
            s6 = str(df.ix[i, 6])
            s7 = str(df.ix[i, 7])
            s8 = str(df.ix[i, 8])
            s9 = str(df.ix[i, 9])
            s10 = str(df.ix[i, 10])
            s11 = str(df.ix[i, 11])
            s12 = str(df.ix[i, 12])
            s13 = str(df.ix[i, 13])
            s14 = str(df.ix[i, 14])
            s15 = str(df.ix[i, 15])
            s16 = str(df.ix[i, 16])
            s17 = str(df.ix[i, 17])

            if len(s8) > 32:
                s8 = s8[:32]
            if len(s5) > 32:
                s5 = s5[:32]
            if len(s7) > 32:
                s7 = s7[:32]
            to_data_q(s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17)


# inputs()
def to_dwxx(s0, s1, s2, s3, s4, s5, s6):
    obj = dwxx(id_qy=s0, name_qy=s1, type=s2, bh=s3, name_fzr=s4, phone=s5, bhs=s6)
    Session.add(obj)
    Session.commit()


def in_put_d():
    print('ok')
    df = pd.read_excel(r'C:\Users\zhouweiqi\Desktop\1\dwxx.xls', sheet_name='Sheet1')
    print(df.index.values)
    print('staring')
    for i in df.index.values:
        print(str(df.ix[i, 1]))

        s0 = str(df.ix[i, 0])
        s1 = str(df.ix[i, 1])
        s2 = str(df.ix[i, 2])
        s3 = str(df.ix[i, 3])
        s4 = str(df.ix[i, 4])
        s5 = str(df.ix[i, 5])
        s6 = str(df.ix[i, 6])

        to_dwxx(s0, s1, s2, s3, s4, s5, s6)

in_put_d()


