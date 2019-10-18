import  pandas as pd
from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker
import os 
import re


# engine=create_engine("mysql+pymysql://root:Runsdata@2017#7v8@server02:3307/fx_data",encoding='utf-8',echo=True)
engine=create_engine("mysql+pymysql://root:Runsdata@2017#7v8@localhost:3307/fx_data",encoding='utf-8',echo=False)
base=declarative_base()



class wzk_all(base):
    __tablename__ = 'wzk_all'
    id               = Column(Integer, primary_key=True)
    id_num           = Column(String(64))
    name             = Column(String(32))
    xingbie          = Column(String(16))
    minzu            = Column(String(16))
    chushengdi       = Column(String(32))
    shengri          = Column(String(32))
    hujitype         = Column(String(32))
    czhkszddz        = Column(String(32))
    tongxundizhi     = Column(String(32))
    youzhengbianma   = Column(String(32))
    lianxidianhua    = Column(String(64))
    renyuanzhuangtai = Column(String(16))
    wenhuachengdu    = Column(String(32))
    gerenbianhua     = Column(String(32))
    danweibianhao    = Column(String(32))
    xingzhenghuafen  = Column(String(16))
    canbaozhuangtai  = Column(String(32))
    zuihuojifei      = Column(String(32))
    daiyukaishijian  = Column(String(32))
    tag              = Column(String(32))
    leixing          = Column(String(32))


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

class user(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    id_num = Column(String(64))


base.metadata.create_all(engine)
Session_class = sessionmaker(bind=engine)
Session = Session_class()


def insert_wsk_all(s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20):
    obj=wzk_all(id_num=s0,name=s1,xingbie=s2, minzu=s3,chushengdi=s4, shengri=s5, hujitype=s6,czhkszddz=s7,tongxundizhi=s8,youzhengbianma=s9,lianxidianhua=s10,   renyuanzhuangtai=s11,  wenhuachengdu=s12,  gerenbianhua=s13,danweibianhao=s14,xingzhenghuafen =s15,canbaozhuangtai=s16,zuihuojifei=s17,daiyukaishijian=s18,tag=s19,leixing= s20)
    Session.add(obj)
    Session.commit()


users=Session.query(user).all()
for i in users:
    print(i.id_num)
    Session.query(data_q).filter(data_q.id_num==i.id_num).
    # for j in data:
    #     print(j.name ,j.id_num)











