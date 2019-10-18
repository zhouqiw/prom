import  csv

with open(r'f:/prom/联通/zjx20191010.csv',encoding='gb2312', errors='ignore') as file:
    reader = csv.DictReader(file)
    print(reader.fieldnames)
    s = [ i for i in reader.fieldnames if i !='']
    # s=s.remove(7)
    del s[7]
    del s[7]
    s.insert(5,'')
    print(type(s))
    print(s)

    for row in reader:
        l = []
        for k,v in row.items():
            # print(v,end=' ')
            l.append(v)

        print(l)
        break
        print(len(l))
        if len(l)!=18:
            print(l)



