#conding:utf-8

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




if __name__ == '__main__':


    base.metadata.create_all(engine)
    Session_class=sessionmaker(bind=engine)
    Session=Session_class()
    # user_obj = user(id_num="rr")
    #104	520201195408094832	黄训德	1	01	大湾镇	19540809	20	大湾派出所	开化村一组79号	553012	6574404	1		10557751	10345926	520201	1		201006

    # print(user_obj.id_num)
    # Session.add(user_obj)
    # print (user_obj.id_num)
    # Session.commit()
    data_obj = data_q(id_num='520201195408094832',name= '黄训德',int_1='1',int_2='01',addr_1='大湾镇',data_b='19540809',int_3='20',addr_pjs='大湾派出所',addr_2='开化村一组79号',int_4='553012',ph_or_te='6574404',int_5='1',int_6='10557751',int_7='10345926',int_8='520201',int_9='1',int_10='201006')
    Session.add(data_obj)
    Session.commit()