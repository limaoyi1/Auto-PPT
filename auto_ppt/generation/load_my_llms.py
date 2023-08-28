# -*- coding: utf-8 -*-
# @Time    : 2023/8/18 9:46
# @Author  : limaoyi
# @File    : llm.py
# @Software: PyCharm
# @GitHub  : https://github.com/limaoyi1/GPT-prompt
import os

import langchain
from langchain.cache import SQLiteCache
from langchain.chat_models import ErnieBotChat, ChatOpenAI

from readconfig.myconfig import MyConfig, ConfigIniError

# 指定编码为 UTF-8
# 获取当前运行的Python文件的绝对路径 对相同的问题进行缓存
current_file_path = os.path.abspath(__file__)

parent_folder = os.path.dirname(os.path.dirname(current_file_path))

sqlite_path = os.path.join(parent_folder, "sqlite")

langchain.llm_cache = SQLiteCache(database_path=sqlite_path)


class LoadMyLLM(object):
    model = None

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        print(model_name)
        self.config = MyConfig()
        if model_name == "" or "gpt-3.5-turbo":
            # 默认使用GPT3.5-turbo
            self._load_gpt_35()
        elif model_name == "gpt-3.5-turbo-16k":
            self._load_gpt_35_16k()
        elif model_name == "gpt-4":
            self._load_gpt_4()
        elif model_name == "ernie-bot":
            self._load_ernie_bot()

        pass

    def run(self):
        return self.model

    def _load_gpt_35(self):
        self._check_openai()
        self.model = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=self.config.OPENAI_API_KEY, streaming=False,
                                temperature=0.7,
                                openai_api_base=self.config.OPENAI_BASE_URL)

    def _load_gpt_35_16k(self):
        self._check_openai()
        self.model = ChatOpenAI(model_name="gpt-3.5-turbo-16k", openai_api_key=self.config.OPENAI_API_KEY,
                                streaming=False,
                                temperature=0.7,
                                openai_api_base=self.config.OPENAI_BASE_URL)

    def _load_gpt_4(self):
        self._check_openai()
        self.model = ChatOpenAI(model_name="gpt-4", openai_api_key=self.config.OPENAI_API_KEY, streaming=False,
                                temperature=0.7,
                                openai_api_base=self.config.OPENAI_BASE_URL)

    def _load_ernie_bot(self):
        self._check_ernie()
        self.model = ErnieBotChat(model_name="ERNIE-Bot-turbo", ernie_client_id=self.config.ERNIE_CLIENT_ID,
                                  ernie_client_secret=self.config.ERNIE_CLIENT_SECRET)

    def _check_openai(self):
        if self.config.OPENAI_API_KEY == "your-openai-api-key":
            raise ConfigIniError("No OPENAI_API_KEY is configured in config")

    def _check_ernie(self):
        if self.config.ERNIE_CLIENT_ID == "your-ernie-client-id":
            raise ConfigIniError("No ERNIE_CLIENT_ID is configured in config")
        if self.config.ERNIE_CLIENT_SECRET == "your-ernie-client-secret":
            raise ConfigIniError("No ERNIE_CLIENT_SECRET is configured in config")


# test
if __name__ == "__main__":
    run = LoadMyLLM(model_name="gpt-3.5-turbo").run()
    predict = run.predict("如何学习java")
    print(predict)
