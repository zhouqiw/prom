from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,ForeignKey,UniqueConstraint,Index
from sqlalchemy.orm import sessionmaker
import time
# engine=create_engine("mysql+pymysql://root:Runsdata@2017#7v8@server02:3307/fx_data",encoding='utf-8',echo=True)
engine=create_engine("mysql+pymysql://root:Runsdata@2017#7v8@localhost:3307/fx_data",encoding='utf-8',echo=False)
base=declarative_base()


class user_wz(base):
    __tablename__ = 'user_wz'
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
    int_12 = Column(String(16))


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


class users(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    id_num = Column(String(64))
    tag = Column(String(10))

base.metadata.create_all(engine)
Session_class = sessionmaker(bind=engine)
Session = Session_class()


def qibianhao():
    tag = Session.query(user_wz).filter(user_wz.int_12 != 'NUll').count()
    print(tag)
    users = Session.query(user_wz).all()
    l = [k[0] for k in Session.query(dwxx.id_qy).all()]
    j = 0
    for i in users:
        if tag < j:
            s = i.int_8[:-2]
            if s in l:
                # print('you in here ={}'.format(s))
                obj = Session.query(user_wz).filter(user_wz.id == i.id).first()
                obj.int_12 = '1'
                Session.commit()
            else:
                obj = Session.query(user_wz).filter(user_wz.id == i.id).first()
                obj.int_12 = '0'
                Session.commit()
        j = j + 1
# qibianhao()


def to_data_wz(s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18):

    obj=(user_wz(id_num=s0, name=s1, int_1=s2, int_2=s3,addr_1=s4, data_b=s5, int_3=s6,addr_pjs=s7, addr_2=s8, int_4=s9, ph_or_te=s10, int_5=s11, int_6=s12,int_7=s13, int_8=s14, int_9=s15, int_10=s16, int_11=s17,int_12=s18))
    Session.add(obj)
    Session.commit()


def orm_cx():
    global tag
    tag = Session.query(user_wz).count()
    w = [k[0] for k in Session.query(users.id_num).filter(users.tag == 0).all()]
    print(w[:20])
    l = w[::-1]
    print(l[:20])
    j = 0
    for i in l:
        if tag <= j:
            # print(i)
            time_start = time.time()
            s = Session.query(data_q).filter(data_q.id_num == i).all()
            print('time cost', time.time() - time_start, 's')

            if len(s) == 0:
                obj = Session.query(users).filter(users.id_num == i).first()
                obj.tag = '3'
                Session.add(obj)
                Session.commit()
                continue
            # print(s)
            # print('-'*30)
            k = s[0]
            to_data_wz(k.id_num, k.name, k.int_1, k.int_2, k.addr_1, k.data_b, k.int_3, k.addr_pjs, k.addr_2, k.int_4,
                       k.ph_or_te, k.int_5, 'NULL', k.int_6, k.int_7, k.int_8, k.int_9, k.int_10, 'NULL')
            obj = Session.query(users).filter(users.id_num == i).first()
            obj.tag = '1'
            Session.add(obj)
            Session.commit()

        j = j + 1


# orm_cx()

