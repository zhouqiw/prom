

with open(r'f:/prom/lt/zjx20190921.txt') as file:
    for s in file.readlines():
        # s = '2019-09-21*移动网*ENODEB*滁州*华为****CUZ-明光大贺郢-F_A类*焦善才*13093326230*焦善才*13093326230***************-750982306*WNMS*1*CUZ31018**OTHER*4G*A*明光市石坝镇大贺郢'
        t = s.split('*')
        # print(t)
        if len(t)!=36:
            print(t)