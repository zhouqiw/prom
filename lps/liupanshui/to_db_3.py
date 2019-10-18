import  pandas as pd
from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker
import  time


# engine=create_engine("mysql+pymysql://root:Runsdata@2017#7v8@server02:3307/fx_data",encoding='utf-8',echo=True)
engine=create_engine("mysql+pymysql://root:Runsdata@2017#7v8@localhost:3307/fx_data",encoding='utf-8',echo=False)
base=declarative_base()

class filename_use_info(base):
    __tablename__ = 'filename_use_info'
    id = Column(Integer, primary_key=True)
    id_num = Column(String(64))
    name = Column(String(32))
    path= Column(String(128))

# base.metadata.create_all(engine)
# Session_class = sessionmaker(bind=engine)
# Session = Session_class()
def to_data(s0,s1,s2):
    obj=filename_use_info(id_num=s0, name=s1, path=s2)
    Session.add(obj)
    Session.commit()





# to_data('522529198812120041','Null','/test/ysxiangbian/new 六枝特区2/六枝特区2/result/ManCheck/522529198812120041[4].jpg')
# print(Session.query(filename_use_info).count())
base.metadata.create_all(engine)
Session_class = sessionmaker(bind=engine)
while 1:


    Session = Session_class()
    print('数据更新条数===>   {}'.format(Session.query(filename_use_info).count()))
    time.sleep(10)