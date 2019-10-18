from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,ForeignKey,UniqueConstraint,Index
from sqlalchemy.orm import sessionmaker
import os
import to_xlsx
import  file_to_path
# engine=create_engine("mysql+pymysql://root:Runsdata@2017#7v8@server02:3307/fx_data",encoding='utf-8',echo=True)
# engine=create_engine("mysql+pymysql://root:Runsdata@2017#7v8@localhost:3307/fx_data",encoding='utf-8',echo=False)
engine=create_engine("mysql+pymysql://root:123456@192.168.159.23:3306/test",encoding='utf-8',echo=False)
base=declarative_base()
class user_jm(base):
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

    tag1 =Session.query(user_jm).filter(user_jm.int_13.like('%jpg%') ).filter(user_jm.int_12==1).count()


    print(tag1)


    # path = '/root'
    path = r'D:\jumimg'
    users = Session.query(user_jm).filter(user_jm.int_13.like('%jpg%') ).filter(user_jm.int_12==1).all()
    file = r'D:\kami1.xlsx'
    for i in users:
        data = [i.id_num ,i.name,i.int_1 ,i.int_2,i.addr_1,i.data_b ,i.int_3 ,i.addr_pjs,i.addr_2,i.int_4,i.ph_or_te,i.int_5,i.int_6,i.int_7,i.int_8,i.int_9,i.int_10,i.int_11,i.int_12,i.int_13 ]
        # print(data)

        file_to_path = str(i.int_8)[:-2] + '_' + str(i.int_7)[:-2]
        print(file_to_path)
        path_0 = os.path.join(path,  file_to_path)
        print(path_0)
        file_slsx = os.path.join(path_0, ('file_to_path'+'.xlsx'))
        print(file_slsx)
        print(file,path_0)
        file_to_path.move_file(file, path_0)
        # print(file_slsx)
        # to_xlsx.w_file(file_slsx,data)
        #












