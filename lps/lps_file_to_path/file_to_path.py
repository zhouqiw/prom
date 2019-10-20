
#conding:utf-8

import  os,time,shutil


def creat_dir(target_dir):
    if not os.path.exists(target_dir):
        print(target_dir + '作为总视频目录不存在，正在创建.....')
        time.sleep(2)
        os.makedirs(target_dir)
        print(target_dir + "总视频目录创建成功")
        time.sleep(2)
def move_file(file,path):
    creat_dir(path)
    if os.path.exists(file):
        shutil.copy(file,path)
    else:
        print('in src file no exists')






if __name__ == '__main__':
    target_dir = '/Users/qizhou/PycharmProjects/prom/77777778_10018829302'
    file_src   = '/Users/qizhou/PycharmProjects/prom'
    file       = 'README.md'
    print(type(target_dir))

    file = os.path.join(file_src,file)
    print(file)
    os.system('rm -rf {}'.format(target_dir))
    # time.sleep(5)
    # move_file(file,target_dir)