# -*- coding: utf-8 -*-
# @Time    : 2023/8/18 15:09
# @Author  : limaoyi
# @File    : other_gen.py
# @Software: PyCharm
# @GitHub  : https://github.com/limaoyi1/GPT-prompt
from generation.load_my_llms import LoadMyLLM
from generation.prompt_templates import LanguageEnum, PolishTemplates


class OptimizeMd:
    llm = None
    language = LanguageEnum.Chinese

    def __init__(self, model_name="gpt-3.5-turbo", language="chinese"):
        self.llm = None
        self.load_my_llm(model_name)
        self.load_language(language)

    def load_my_llm(self, model_name="gpt-3.5-turbo"):
        if model_name == "gpt-3.5-turbo":
            self.llm = LoadMyLLM(model_name).run()
            return

    def load_language(self, language: str = "chinese"):
        if language == "chinese" or language == "chs":
            self.language = LanguageEnum.Chinese
        elif language == "english":
            self.language = LanguageEnum.English

    # 智能改写
    def smart_rewrite(self, markdown_string):
        print("\033[92m\033[1m" + "\n*****Smart Rewrite*****\n" + "\033[0m\033[0m")
        rewrite_template = PolishTemplates(markdown_string).build(self.language)
        rewrite = self.llm.predict(rewrite_template)
        print(rewrite)
        print("\033[95m\033[1m" + "\n*****Rewrite Over*****\n" + "\033[0m\033[0m")
        return rewrite
