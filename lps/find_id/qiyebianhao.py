from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,ForeignKey,UniqueConstraint,Index
from sqlalchemy.orm import sessionmaker
# engine=create_engine("mysql+pymysql://root:Runsdata@2017#7v8@server02:3307/fx_data",encoding='utf-8',echo=True)
# engine=create_engine("mysql+pymysql://root:Runsdata@2017#7v8@localhost:3307/fx_data",encoding='utf-8',echo=False)
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


def run(cls_var):
    base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    Session = Session_class()
    tag1 = Session.query(cls_var).filter(cls_var.int_12 =='1').count()
    print(tag1)
    tag = Session.query(cls_var).filter(cls_var.int_12 != 'NUll').count()-89205
    print(tag)
    users = Session.query(cls_var).all()
    l = [k[0] for k in Session.query(dwxx.id_qy).all()]
    j = 0
    for i in users:
        if tag1 < j:
            s = i.int_8[:-2]
            if s in l:
                print('you in here ={}'.format(s))
                obj = Session.query(cls_var).filter(cls_var.id == i.id).first()
                obj.int_12 = '1'
                Session.commit()
            else:
                obj = Session.query(cls_var).filter(cls_var.id == i.id).first()
                obj.int_12 = '0'
                Session.commit()
        if j%100==0:
            print(j)
        j = j + 1

if __name__ == '__main__':
    run(user_zg)
    # run(user_zg)
    # run(user_zg)





