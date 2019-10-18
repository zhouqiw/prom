import  csv

with open(r'f:/prom/联通/zjxcell20191010.csv',encoding='gb2312', errors='ignore') as file:
    reader = csv.DictReader(file)
    print(reader.fieldnames)
    s = [ i for i in reader.fieldnames if i !='']
    s.insert(7, '')
    print(type(s))
    print(s)
    print(len(s))

    for row in reader:
        # l = []
        # for k,v in row.items():
        #     # print(v,end=' ')
        #     l.append(v)
        #
        l = [v for k, v in row.items()]
        if len(l)>12:
            # print(l)
            # print(l[:11])
            k = ''
            for i in l[11:]:
                # print(i)
                if type(i)==str:
                    k = k + '-' + i
                elif type(i)==list:
                    for j in i:
                        k = k +'-'+ j
            print(k)
            p = l[:11]
            p.insert(11,k)
            print(p)
        if len(l)==12:
            print(l)



