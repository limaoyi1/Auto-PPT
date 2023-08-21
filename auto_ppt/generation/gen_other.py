# -*- coding: utf-8 -*-
# @Time    : 2023/8/18 15:09
# @Author  : limaoyi
# @File    : other_gen.py
# @Software: PyCharm
# @GitHub  : https://github.com/limaoyi1/GPT-prompt
from generation.load_my_llms import LoadMyLLM
from generation.prompt_templates import LanguageEnum, PolishTemplates, VerbatimTemplates, DataCollectionTemplates
from mdtree.parser import Parser


class OptimizeMd:
    llm = None
    language = LanguageEnum.Chinese

    def __init__(self, model_name="gpt-3.5-turbo", language="chinese"):
        self.llm = None
        self.load_my_llm(model_name)
        self.load_language(language)

    def load_my_llm(self, model_name="gpt-3.5-turbo"):
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

    # 智能表格
    def smart_form(self, markdown_string):
        print("\033[92m\033[1m" + "\n*****Smart Form*****\n" + "\033[0m\033[0m")
        form_template = DataCollectionTemplates(markdown_string).build(self.language)
        form = self.llm.predict(form_template)
        print(form)
        print("\033[95m\033[1m" + "\n*****Gen Over*****\n" + "\033[0m\033[0m")
        return form

    # 生成逐字稿
    def generate_verbatim(self, markdown_string):
        print("\033[92m\033[1m" + "\n*****Gen Verbatim*****\n" + "\033[0m\033[0m")
        parser = Parser()
        parser.parse(markdown_string)
        out = parser.out
        main = out.main
        self._generate_chapter(main)
        print("\033[95m\033[1m" + "\n*****Gen Over*****\n" + "\033[0m\033[0m")
        return self.result

    result: list[str] = []

    def _generate_chapter(self, heading):
        if heading is not None and (heading.children is None or heading.children == []):
            verbatim_template = VerbatimTemplates(heading.source).build(self.language)
            verbatim = self.llm.predict(verbatim_template)
            print(verbatim)
            self.result.append(verbatim)
        elif heading is not None and (heading.source is None or heading.source == ''):
            content = ""
            if heading.children is not []:
                for child in heading.children:
                    content = content + child.text + "\n"
            verbatim_template = VerbatimTemplates(content).build(self.language)
            verbatim = self.llm.predict(verbatim_template)
            print(verbatim)
            self.result.append(verbatim)

        # self.make_slide_demo(self.prs, heading.text, heading.source)
        if heading.children is not []:
            for child in heading.children:
                self._generate_chapter(child)


if __name__ == "__main__":
    str1 = """#  开源项目维护之道：解锁代码自由
## 概述
### 介绍开源项目的概念和重要性

开源项目指的是可以被公开查看、使用、修改和分发的软件项目。开源项目的重要性在于它们提供了一种共享知识和合作的模式，促进了创新和技术进步。

开源项目的定义

开源项目是指其源代码可以被公开查看、使用、修改和分发的软件项目。这意味着任何人都可以参与其中并为其改进和发展做出贡献。

开源项目的优势

开源项目有许多优势。首先，它们提供了一种共享知识和合作的模式，使得更多的人能够参与到软件开发中来。其次，开源项目可以获得更多的反馈和测试，从而提高软件的质量和可靠性。此外，开源项目还可以帮助解决技术难题，推动技术进步。

开源项目的影响和贡献

开源项目的影响力不可忽视。许多重要的软件和技术都是由开源项目推动和发展而来的。同时，开源项目也为社区提供了一个学习和分享的平台，每个人都可以从中获得知识和经验。

![开源](https://source.unsplash.com/1000x600/?open+source)
## 基本原则
### 开源社区的价值观

开源社区的价值观是指在开源软件开发和使用过程中，所遵循的一些核心价值观念。这些价值观包括透明、协作、共享和互助。开源社区通过共享源代码、协同工作和互相支持，不仅提供了高质量的软件，也促进了技术的进步和社区的发展。

![开源社区](https://source.unsplash.com/1000x600/?opensource-community)

### 遵循开源许可证

遵循开源许可证是开源软件开发的基本原则之一。开源许可证是一种法律工具，它规定了开源软件的使用、修改和分发的条件。遵循开源许可证可以保护开源软件的自由和开放，并确保开发者和用户之间的权益得到保障。

![开源许可证](https://source.unsplash.com/1000x600/?opensource-license)

### 维护良好的代码仓库管理

维护良好的代码仓库管理是保证开源项目顺利进行的重要环节。一个良好的代码仓库管理包括代码版本控制、代码文档化、问题追踪等方面。通过维护良好的代码仓库管理，可以提高开发效率，降低维护成本，保证项目的可持续发展。

![代码仓库管理](https://source.unsplash.com/1000x600/?code-repository)

"""
    md = OptimizeMd(model_name="gpt-3.5-turbo-16k")
    form= md.smart_form(
        "开源项目的影响和贡献\n开源项目的影响力不可忽视。许多重要的软件和技术都是由开源项目推动和发展而来的。同时，开源项目也为社区提供了一个学习和分享的平台，每个人都可以从中获得知识和经验。")
    print(form)
    # run = md.generate_verbatim(str1)
    # for i in run:
    #     print("\033[95m\033[1m" + "\n*****chapter*****\n" + "\033[0m\033[0m")
    #     print(i)
