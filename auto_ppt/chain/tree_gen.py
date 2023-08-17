# -*- coding: utf-8 -*-
# @Time    : 2023/8/16 16:47
# @Author  : limaoyi
# @File    : tree_gen.py
# @Software: PyCharm
# @GitHub  : https://github.com/limaoyi1/GPT-prompt
from langchain import OpenAI
from langchain.callbacks import StreamingStdOutCallbackHandler

from mdtree.parser import parse_string
from readconfig.myconfig import MyConfig


class TreeGen:
    def __init__(self, md_str):
        self.out = None
        self.tree = None
        self.md_str = md_str
        self.config = MyConfig()
        self.init_markdown(self.md_str)

    def init_markdown(self, md_str):
        self.md_str = md_str
        self.out = parse_string(md_str)
        self.tree = self.out.main
        self.traverse_tree(self.tree)

    def traverse_tree(self, heading):
        if heading is None:
            print("heading为空")
            return
        # self.make_slide_demo(self.prs, heading.text, heading.source)
        if len(heading.children) > 0:
            for child in heading.children:
                self.traverse_tree(child)
        elif len(heading.children) == 0:
            text = heading.text
            source = heading.source
            title = heading.root.main.text
            template: str = f"""帮助我完成标题为{text}的markdown文章片段.文章用于生成一个演示PPT.使用markdown的格式表达文本内容,不允许创建标题,简明扼要的根据标题生成文本,可以加入有趣的案例、实例、表格数据或引用，以支持您的论点。
输出内容之后,需要使用unsplash在内容下一行，增加一张合适的主题配图，格式为:![主题](https://source.unsplash.com/1000x600/?+英文主题).
不要返回其他内容,方便我直接插入markdown.保持内容的简洁.
"""
            llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=self.config.OPENAI_API_KEY, streaming=True,
                         openai_url_base=self.config.OPENAI_BASE_URL,
                         callbacks=[StreamingStdOutCallbackHandler()])
            predict = llm.predict(template)
            heading.add_source(predict)
            return

    def output(self):
        return self.tree.full_source
        pass


if __name__ == '__main__':
    md = """# 初学者骑车之路：掌握自行车技巧的必备指南 

## 自行车基础知识

### 自行车的组成部分
"""
    gen = TreeGen(md)
    print(gen.output())

