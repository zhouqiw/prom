# encoding: utf-8
import configparser

class ReadConfig:
    def __init__(self,env):
        self.env = env
        self.url = None
        self.receive = None
        self.config_file_name = 'env.ini'

    def read(self):
        cf = configparser.ConfigParser()
        cf.read(self.config_file_name)
        self.url = cf.get(self.env, 'url')
        self.receive = cf.get(self.env, 'receive')
        return {'url': self.url, 'receive': self.receive}

    def run(self):
        return self.read()


if __name__ == '__main__':
    readconfig = ReadConfig('test')
    print(readconfig.run())