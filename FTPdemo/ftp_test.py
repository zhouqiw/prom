# -*-coding:utf-8-*-

import os
import time
from ftplib import FTP

FTP_SERVER = 'xx.xx.xx.xx'
USER = '用户'
PWD = '密码'
FTP_PATH = '/home/xx/xx/'
local_root = 'e:' + FTP_PATH
DATE = time.strftime('%Y%m%d', time.localtime(time.time()))
print DATE

def isDir(filename):
    try:
        path = filename;
        path.replace('/', '\\')
        if os.path.exists(path):
            print
            '---file exists--'
        else:
            print            'file not exists ', local_root
            os.mkdirs(local_root)
        return True
    except:
        return False


def ftpconnect():
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect(FTP_SERVER, 21)
    ftp.login(USER, PWD)
    return ftp


def downloadfile():
    ftp = ftpconnect()
    print  ftp.getwelcome()  # 显示ftp服务器欢迎信息

    li = ftp.nlst(FTP_PATH)
    print  'ftp: ', li
    for eachfile in li:
        localpath = 'e:' + eachfile
        print        '-- open localpath --', localpath
        bufsize = 1024
        isDir(localpath)
        fp = open(localpath, 'wb+')
        ftp.retrbinary('RETR ' + eachfile, fp.write, bufsize)
        fp.flush()

    ftp.set_debuglevel(0)  # 关闭调试
    fp.close()
    ftp.quit()  # 退出ftp服务器


if __name__ == "__main__":
    downloadfile()