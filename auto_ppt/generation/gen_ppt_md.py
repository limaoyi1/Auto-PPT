# -*- coding: utf-8 -*-
# @Time    : 2023/8/17 10:10
# @Author  : limaoyi
# @File    : gen_ppt_md.py
# @Software: PyCharm
# @GitHub  : https://github.com/limaoyi1/GPT-prompt
from langchain import OpenAI

from generation.load_my_llms import LoadMyLLM
from generation.prompt_templates import TitleTemplates, LanguageEnum, OutlineTemplates, OutlineFormatTemplates, \
    MaterialCollectionTemplates, CompletionTemplates, get_first_line
from mdtree.parser import Parser
from readconfig.myconfig import MyConfig

#  全新的架构方式, 后端只负责生成md, 前端负责转换markdown为PPT
## 去掉对redis的依赖,保证可以打包作为工具,降低用户依赖

class GenMd:
    llm = None
    language = LanguageEnum.Chinese
    title = ""
    outline = ""
    format_outline = ""
    materials = ""
    total_text = ""

    # 任务list 完成多个任务:
    # 获取预设用户信息
    # 收集信息
    # 生成标题
    # 生成大纲
    # 校对大纲
    # 生成全文 tree
    # 需要校对全文吗?

    def __init__(self, profession, topic, model_name="gpt-3.5-turbo", language="chinese"):
        self.profession = profession
        self.topic = topic
        self.llm = None
        self.load_my_llm(model_name)
        self.load_language(language)

    def run(self):
        self.gen_title()
        self.gen_outline()
        self.format_cleanup_outline()
        # self.material_collection() 难以获取到真实数据
        self.tree_to_md()
        return self.total_text

    # 支持切换多种模型
    def load_my_llm(self, model_name="gpt-3.5-turbo"):
        if model_name == "gpt-3.5-turbo":
            self.llm = LoadMyLLM(model_name).run()
            return

    def load_language(self, language: str = "chinese"):
        if language == "chinese" or language == "chs":
            self.language = LanguageEnum.Chinese
        elif language == "english":
            self.language = LanguageEnum.English

    def gen_title(self):
        print("\033[92m\033[1m" + "\n*****Gen Title*****\n" + "\033[0m\033[0m")
        title_template = TitleTemplates(self.profession, self.topic).build(self.language)
        title = self.llm.predict(title_template)
        print(title)
        self.title = title
        print("\033[95m\033[1m" + "\n*****Gen Over*****\n" + "\033[0m\033[0m")

    def gen_outline(self):
        print("\033[92m\033[1m" + "\n*****Gen Outline*****\n" + "\033[0m\033[0m")
        outline_template = OutlineTemplates(self.profession, self.topic, self.title).build(self.language)
        outline = self.llm.predict(outline_template)
        print(outline)
        self.outline = outline
        print("\033[95m\033[1m" + "\n*****Gen Over*****\n" + "\033[0m\033[0m")

    def format_cleanup_outline(self):
        print("\033[92m\033[1m" + "\n*****Format Outline*****\n" + "\033[0m\033[0m")
        outline_template = OutlineFormatTemplates(self.outline).build(self.language)
        format_outline = self.llm.predict(outline_template)
        print(format_outline)
        self.format_outline = format_outline
        print("\033[95m\033[1m" + "\n*****Format Over*****\n" + "\033[0m\033[0m")

    def material_collection(self):
        material_template = MaterialCollectionTemplates(self.format_outline).build(self.language)
        materials = self.llm.predict(material_template)
        self.materials = materials

    def tree_to_md(self):
        print("\033[92m\033[1m" + "\n*****Gen Total*****\n" + "\033[0m\033[0m")
        # 减少api调用次数 只对二级标题进行遍历
        Parser(self.format_outline)
        parser = Parser()
        parser.parse(self.format_outline)
        out = parser.out
        # 获取第一级
        total_text = ""
        main = out.main
        if main.level == 1:
            total_text += "# " + main.text + "\n"
            # 获取第二级
            childrens = main.children
            for child in childrens:
                # print(child.full_source)
                completion_template = CompletionTemplates(child.full_source).build(self.language)
                completion = self.llm.predict(completion_template)
                first_line = get_first_line(child.full_source)
                total_text += first_line + "\n"
                total_text += completion + "\n"
        self.total_text = total_text
        print(total_text)
        print("\033[95m\033[1m" + "\n*****Gen Over*****\n" + "\033[0m\033[0m")


if __name__ == "__main__":
    md = GenMd("新人主播", "新人主播如何进行直播")
    run = md.run()
    print(run)
