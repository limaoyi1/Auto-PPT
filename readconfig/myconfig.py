import codecs
import configparser
config = configparser.ConfigParser()
# 指定编码为 UTF-8


class MyConfig:
    Real_File: str = None
    OPENAI_BASE_URL: str = None
    OPENAI_API_KEY: str = None
    UNSPLASH_ENABLE: str = None
    UNSPLASH_API_KEYS: list = None
    REDIS_ENABLE: str = None
    REDIS_URL: str = None

    def __init__(self):
        config.read_file(codecs.open('config.ini', 'r', 'utf-8-sig'))
        self.Real_File = config.get('Credentials', 'Real_File')
        if self.Real_File == "Config.ini":
            self.OPENAI_BASE_URL = config.get('Credentials', 'OPENAI_BASE_URL')
            self.OPENAI_API_KEY = config.get('Credentials', 'OPENAI_API_KEY')
            self.UNSPLASH_API_KEYS = config.get('Credentials', 'UNSPLASH_API_KEYS').split(',')
            self.UNSPLASH_ENABLE = config.get('Credentials', 'UNSPLASH_ENABLE')
            self.REDIS_ENABLE = config.get('Credentials', 'REDIS_ENABLE')
            self.REDIS_URL = config.get('Credentials', 'REDIS_URL')
        else:
            config.read_file(codecs.open(self.Real_File, 'r', 'utf-8-sig'))
            self.OPENAI_BASE_URL = config.get('Credentials', 'OPENAI_BASE_URL')
            self.OPENAI_API_KEY = config.get('Credentials', 'OPENAI_API_KEY')
            self.UNSPLASH_API_KEYS = config.get('Credentials', 'UNSPLASH_API_KEYS').split(',')
            self.UNSPLASH_ENABLE = config.get('Credentials', 'UNSPLASH_ENABLE')
            self.REDIS_ENABLE = config.get('Credentials', 'REDIS_ENABLE')
            self.REDIS_URL = config.get('Credentials', 'REDIS_URL')
        print(self.OPENAI_API_KEY)

if __name__ == '__main__':
    my_config = MyConfig()
    print(my_config.REDIS_ENABLE)
