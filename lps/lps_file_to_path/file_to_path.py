import  os,time,shutil


def creat_dir(target_dir):
    if not os.path.exists(target_dir):
        print(target_dir + '作为总视频目录不存在，正在创建.....')
        time.sleep(2)
        os.mkdir(target_dir)
        print(target_dir + "总视频目录创建成功")
        time.sleep(2)
def move_file(file,path):
    creat_dir(path)
    if os.path.exists(file):
        shutil.copy(file,path)
    else:
        print('in src file no exists')






if __name__ == '__main__':
    target_dir = r'F:\sstest'
    file_src = 'd.txt'
    path_target=r'F:\stest'

    file = os.path.join(target_dir,file_src)
    print(file)

    move_file(file,path_target)