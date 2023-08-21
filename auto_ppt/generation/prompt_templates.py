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
大纲的全部由标题组成(\"#,##\")和无序列表(\"-,*\")组成,标题不能超过3级.
```markdown"""
        self.english = f"""I want you to act as a {profession} and prepare a presentation in front of an audience on the topic {topic}.
You have written a title {title} for your powerpoint presentation. Now you need to write an outline in markdown format.
All outline is composed of the title (\ "#, ##\") and unordered list (\ "-- - * \"), the title should not exceed 3.
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
        self.english = f"""You are a Markdown formatting AI, responsible for formatting, proofreading syntax, and polishing headings. You need to modify the original markdown to a new markdown consisting entirely of headings (\"#,##,###\"). 
If the original markdown has unordered lists (-, *) or ordered lists (1.), create a subhead (\"##,###,####\") to replace the original list. Remove characters from unordered or ordered lists ("-, *,1." etc.) 
I hope you can replace my A0 simplified words and sentences with more elegant and advanced words and sentences, keeping the same meaning and making the title more literary.
I need you to delete the notes and information irrelevant to the topic, and organize the outline to make it more streamlined.
Here is the original markdown:
```markdown 
{outline}
```
New markdown: """


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
        self.english = f"""You're an encyclopedic retrieval AI that helps people with materials they might need to write about, such as papers, current events, conclusions, or data. I'll give you an outline of the article, and you'll need to retrieve 10 possible sources.
You need to label each piece of data with a specific source. Don't try to fudge the truth.
Here's my outline:
```markdown
{outline}
` ` `
Material :"""


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
每一个最小子标题都需要使用unsplash在子标题的下一行，增加一张合适的主题配图，格式为:![主题](https://source.unsplash.com/1000x600/?+英文主题).
不要返回其他内容,方便我直接插入markdown.
新的markdown:
{first_line}"""
        self.english = f""" You are an experienced PPT writer who is good at helping others write a complete presentation and provide it through markdown's code.
Don't allow you to create a title, brief and to the point, according to the kid title (###,####) to generate text, not according to the second-level heading to generate text (##)
You can include interesting cases, examples, tabular data, or quotes to support your argument. Keep your content simple and elegant
Here are a few simple slides
```markdown
{outline}
` ` `
For each subtitle, use unsplash to add an appropriate theme image to the next line of content in the format :! [subject] (https://source.unsplash.com/1000x600/?+ English topic).
Don't return anything else, so I can just insert markdown.
New markdown:
{first_line}"""


class PolishTemplates(PromptTemplates):
    def __init__(self, markdown_str):
        super().__init__()
        self.chinese = f"""我希望你能成为一名专业的拼写和语法纠错者和改进者。
我想让你用更漂亮优雅的中文词语和句子代替我的简化的a0级词语和句子。
保持意思不变，不要改变我文章的结构，但使它们更有文学性或者学术性，并提高我作为行业专家的风格表达。
这是我的降价:
```markdown
{markdown_str}
```
新markdown:"""
        self.english = f"""I want you to act as an professional spelling and grammer corrector and improver.
I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level English words and sentences.
Keep the meaning the same, don't change the structure of my articles, but make them more literary or academic, and improve my style of presentation as an industry expert.
This is my markdown:
```markdown
{markdown_str}
```
new markdown:"""


def get_first_line(input_string):
    lines = input_string.split('\n')
    if lines:
        return lines[0].strip()
    else:
        return ""


class VerbatimTemplates(PromptTemplates):
    def __init__(self, markdown_str):
        super().__init__()
        self.chinese = f"""我希望你能成为一名逐字稿编写AI,为我的PPT写成一篇逐字稿。我会把我的PPT文本内容用markdown的方式告诉你.
你需要生成一篇逐字稿文章段落介绍某一张幻灯片中的内容:
```markdown
{markdown_str}
```
我想让你用使用更口语化的语言和更风趣幽默,更有感染力的风格.
保持意思不变和内容的简洁，并提高我作为行业专家的风格表达。
逐字稿:"""
        self.english = f"""I hope you can become a verbatim writing AI and write a verbatim draft for my PPT. I will tell you my PPT text content in markdown.
You need to generate a verbatim article paragraph describing the content of a certain slide:
```markdown
{markdown_str}
```
I want you to use a more colloquial language and a more humorous and infectious style.
Keep the meaning constant and the content concise, and improve my stylistic expression as an industry expert.
Transcript:"""


class DataCollectionTemplates(PromptTemplates):
    def __init__(self, markdown_str):
        super().__init__()
        self.chinese = f"""我希望你成为一个数据检索引擎,我会给你主题内容,你需要给我一组或者多组数据帮助我论证我的观点.你需要提供数据的来源和时间.你需要使用markdown的表格格式返回.
不要试图编造数据,如果没有检索到,请返回"我没有检索到数据"
这是我的主题:
```markdown
{markdown_str}
```
数据:
"""
