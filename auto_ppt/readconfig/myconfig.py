# -*- coding: utf-8 -*-
# @Time    : 2023/8/17 10:10
# @Author  : limaoyi
# @File    : gen_ppt_md.py
# @Software: PyCharm
# @GitHub  : https://github.com/limaoyi1
import codecs
import configparser
import os

config = configparser.ConfigParser()
# 指定编码为 UTF-8
# 获取当前运行的Python文件的绝对路径
current_file_path = os.path.abspath(__file__)

base = current_file_path.replace("myconfig.py", "") + "../"


class ConfigIniError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MyConfig:
    OPENAI_BASE_URL: str = None
    OPENAI_API_KEY: str = None
    UNSPLASH_ENABLE: str = None
    ERNIE_CLIENT_ID: str = None
    ERNIE_CLIENT_SECRET: str = None

    def __init__(self):
        if os.path.exists(base + "lmy_config.ini"):
            config.read_file(codecs.open(base + "lmy_config.ini", 'r', 'utf-8-sig'))
            self.OPENAI_BASE_URL = config.get('Credentials', 'OPENAI_BASE_URL')
            self.OPENAI_API_KEY = config.get('Credentials', 'OPENAI_API_KEY')
            self.UNSPLASH_ENABLE = config.get('Credentials', 'UNSPLASH_ENABLE')
            self.ERNIE_CLIENT_ID = config.get('Credentials', 'ERNIE_CLIENT_ID')
            self.ERNIE_CLIENT_SECRET = config.get('Credentials', 'ERNIE_CLIENT_SECRET')
            print("My Config:", base + "lmy_config.ini")
        else:
            config.read_file(codecs.open(base + 'config.ini', 'r', 'utf-8-sig'))
            self.OPENAI_BASE_URL = config.get('Credentials', 'OPENAI_BASE_URL')
            self.OPENAI_API_KEY = config.get('Credentials', 'OPENAI_API_KEY')
            self.UNSPLASH_ENABLE = config.get('Credentials', 'UNSPLASH_ENABLE')
            self.ERNIE_CLIENT_ID = config.get('Credentials', 'ERNIE_CLIENT_ID')
            self.ERNIE_CLIENT_SECRET = config.get('Credentials', 'ERNIE_CLIENT_SECRET')
            print("My Config:", base + 'config.ini')


if __name__ == '__main__':
    my_config = MyConfig()
    print(my_config.REDIS_ENABLE)
