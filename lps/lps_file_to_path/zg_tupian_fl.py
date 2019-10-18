from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,ForeignKey,UniqueConstraint,Index
from sqlalchemy.orm import sessionmaker
import os
import  file_to_path
# engine=create_engine("mysql+pymysql://root:Runsdata@2017#7v8@server02:3307/fx_data",encoding='utf-8',echo=False)
#engine=create_engine("mysql+pymysql://root:Runsdata@2017#7v8@localhost:3307/fx_data",encoding='utf-8',echo=False)
engine=create_engine("mysql+pymysql://root:123456@192.168.159.23:3306/test",encoding='utf-8',echo=False)
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
    int_12 = Column(String(16))
    int_13 = Column(String(16))


class filename_use_infos(base):
    __tablename__ = 'filename_use_infos'
    id = Column(Integer, primary_key=True)
    id_num = Column(String(64))
    name = Column(String(32))
    path= Column(String(128))



if __name__ == '__main__':

    base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    Session = Session_class()

    tag1 =Session.query(user_zg).filter(user_zg.int_13.like('%jpg%') ).filter(user_zg.int_12==1).count()


    print(tag1)


    # path = '/test'
    #
    # users = Session.query(user_zg).filter(user_zg.int_13.like('%jpg%') ).filter(user_zg.int_12==1).all()
    #
    # for i in users:
    #     # print(i.int_13,)
    #     path_0 = os.path.join(path, ('zhigong'+'/' + str(i.int_8)[:-2]+'_'+ str(i.int_7)[:-2]))
    #     print(path_0)
    #     file_to_path.move_file(i.int_13,path_0)









