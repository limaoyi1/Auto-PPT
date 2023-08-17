# -*- coding: utf-8 -*-
# @Time    : 2023/8/17 10:57
# @Author  : limaoyi
# @File    : prompt_templates.py
# @Software: PyCharm
# @GitHub  : https://github.com/limaoyi1/GPT-prompt
from enum import Enum


class LanguageEnum(Enum):
    Chinese = "chinese"
    English = "english"


class PromptTemplates:
    chinese = None
    english = None

    def __init__(self):
        pass

    def build(self, language=LanguageEnum.English):
        if language == LanguageEnum.English:
            return self.english
        elif language == LanguageEnum.Chinese:
            return self.chinese


class TitleTemplates(PromptTemplates):

    def __init__(self, profession, topic):
        super().__init__()
        self.chinese = f"""我希望你扮演一名{profession},准备在听众面前进行演示报告,话题是{topic},首先你需要为你的演示报告PPT写一个引人注目并且简洁优雅的标题."""
        self.english = f"""I want you to act as a {profession} and prepare to give a presentation report in front of the audience. The topic is {topic}. First of all, you need to write a catchy, concise and elegant title for your presentation report PPT."""


class OutlineTemplates(PromptTemplates):

    def __init__(self, profession, topic, title):
        super().__init__()
        self.chinese = f"""我希望你扮演一名{profession},准备在听众面前进行演示报告,话题是{topic}.
你已经为你的演示报告PPT写一个标题{title}.现在你需要用markdown的格式写一个大纲.
大纲的全部由标题组成(\"#,##,###\")和无序列表(\"-,*\")组成,标题不能超过3级.
```markdown"""


class OutlineFormatTemplates(PromptTemplates):

    def __init__(self, outline):
        super().__init__()
        self.chinese = f"""你是一个Markdwon格式修改人工智能,负责修改格式,校对语法,并且润色标题内容,你需要把原markdown全部修改为全部由标题组成(\"#,##,###\")的新markdown.
如果原markdown还有无序列表(-,*)或者有序列表(1.),创建子标题(\"##,###,####\")的方式代替原来的列表.删除无序或者有序列表("-,*,1."等)的字符
我希望你使用更加优雅高级的词语和句子替换我的A0级简化的词语和句子,保持句子意思不变,使标题更具有文学性.
我需要你删除与主题无关的注释和信息,整理大纲让大纲更加流程
这是原markdown:
```markdown
{outline}
```
新markdown:"""


class MaterialCollectionTemplates(PromptTemplates):
    def __init__(self, outline):
        super().__init__()
        self.chinese = f"""你是一个百科全书式的检索AI,帮助人们写作时可能需要使用到的素材,例如论文,时事,结论或者数据.我会给你文章的大纲,你需要检索到10个可能会使用到的素材.
你需要对每一个数据标注具体的来源.不要试图捏造事实.
这是我的大纲:
```markdown
{outline}
```
素材:"""


class CompletionTemplates(PromptTemplates):
    def __init__(self, outline):
        super().__init__()
        first_line = get_first_line(outline)
        self.chinese = f"""你是一名资深的PPT撰写专家，擅长帮助别人撰写一份完整演示文档，并且通过markdown的代码来提供.
不允许创建标题,简明扼要的根据最小子标题(###,####)生成文本,不要根据第二级标题生成文本(##)
可以加入有趣的案例、实例、表格数据或引用，以支持您的论点.保持内容的简洁和优雅
这是几张简单的幻灯片
```markdown
{outline}
```
每一个最小子标题都需要使用unsplash在内容的下一行，增加一张合适的主题配图，格式为:![主题](https://source.unsplash.com/1000x600/?+英文主题).
不要返回其他内容,方便我直接插入markdown.
新的markdown:
{first_line}"""

def get_first_line(input_string):
    lines = input_string.split('\n')
    if lines:
        return lines[0].strip()
    else:
        return ""