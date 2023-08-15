import codecs
import configparser
import os

config = configparser.ConfigParser()
# 指定编码为 UTF-8

base = "E:\\LocalWarehouse\\github\\Auto-PPT\\auto_ppt\\"


class MyConfig:
    Real_File: str = None
    OPENAI_BASE_URL: str = None
    OPENAI_API_KEY: str = None
    UNSPLASH_ENABLE: str = None
    UNSPLASH_API_KEYS: list = None
    REDIS_ENABLE: str = None
    REDIS_URL: str = None

    def __init__(self):
        current_path = os.getcwd()
        print("当前路径:", current_path)
        config.read_file(codecs.open(base+'config.ini', 'r', 'utf-8-sig'))
        self.Real_File = config.get('Credentials', 'Real_File')
        if self.Real_File == "Config.ini":
            self.OPENAI_BASE_URL = config.get('Credentials', 'OPENAI_BASE_URL')
            self.OPENAI_API_KEY = config.get('Credentials', 'OPENAI_API_KEY')
            self.UNSPLASH_API_KEYS = config.get('Credentials', 'UNSPLASH_API_KEYS').split(',')
            self.UNSPLASH_ENABLE = config.get('Credentials', 'UNSPLASH_ENABLE')
            self.REDIS_ENABLE = config.get('Credentials', 'REDIS_ENABLE')
            self.REDIS_URL = config.get('Credentials', 'REDIS_URL')
        else:
            config.read_file(codecs.open(base+self.Real_File, 'r', 'utf-8-sig'))
            self.OPENAI_BASE_URL = config.get('Credentials', 'OPENAI_BASE_URL')
            self.OPENAI_API_KEY = config.get('Credentials', 'OPENAI_API_KEY')
            self.UNSPLASH_API_KEYS = config.get('Credentials', 'UNSPLASH_API_KEY').split(',')
            self.UNSPLASH_ENABLE = config.get('Credentials', 'UNSPLASH_ENABLE')
            self.REDIS_ENABLE = config.get('Credentials', 'REDIS_ENABLE')
            self.REDIS_URL = config.get('Credentials', 'REDIS_URL')
        print(self.OPENAI_API_KEY)

if __name__ == '__main__':
    my_config = MyConfig()
    print(my_config.REDIS_ENABLE)
