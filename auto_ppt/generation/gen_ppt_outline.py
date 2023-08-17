import uuid

from langchain import OpenAI
from langchain.callbacks import StreamingStdOutCallbackHandler

from chain.tree_gen import TreeGen
from mdtree.tree2ppt import Tree2PPT
from readconfig.myconfig import MyConfig
from chain.gpt_memory import GptChain


# 抽象父类
class Gen:
    config: MyConfig = None
    GptChain: GptChain = None

    def __init__(self, session_id):
        self.config = MyConfig()
        print(f"open ai key:{self.config.OPENAI_API_KEY}")
        self.GptChain = GptChain(openai_api_key=self.config.OPENAI_API_KEY, session_id=session_id,
                                 redis_url=self.config.REDIS_URL,openai_url_base=self.config.OPENAI_BASE_URL)


# ----------------------------------------------------------------
# 生成标题
class GenTitle(Gen):
    def __init__(self, session_id):
        super().__init__(session_id)

    def predict_title(self, query):
        text = f"""我希望你帮助我以```{query}```为话题生成3个PPT的备选的标题.要求能吸引人的注意.
        """
        return self.GptChain.predict(text)

    def predict_title_v2(self, form, role, title1, topic_num=1):
        text = f"""我是一名{role},正在制作一个关于{form}的{title1}PPT,我计划先写一个markdown来完成PPT中的文本部分.现在帮助我写{topic_num}个备选的标题.我会中其中选择一个.
要求:标题吸引人注目,并且具有创意,标题之间使用\"\\n\"分隔,只需要返回标题,不要问我具体内容"""
        return self.GptChain.predict(text)


class GenOutline(Gen):
    def __init__(self, session_id):
        super().__init__(session_id)

    def predict_outline(self, query):
        text = f"""我选择的标题是第```{query}```个标题,我希望你用markdown的格式生成大纲,并且请遵循以下要求:
1.只需要创建标题，请在单词或短语前面添加井号 (#) 。# 的数量代表了标题的级别；
2.不能使用无序或者有序列表,必须全部使用添加井号 (#)的方式表示大纲结构；
3.第一级(#)表示大纲的标题,第二级(##)表示章节的标题,第三级(###)表示章节的重点；
4.大纲的第一章是```{query}```的简介，最后一章是总结；
        """
        return self.GptChain.predict(text)

    def predict_outline_v2(self, title, title_requirement):
        text = f"""请根据标题<{title}>和以下内容，为我生成一个只包含标题的有效大纲。请确保大纲的每一部分都是以 Markdown 格式的标题 (#, ##, ###, ####) 组成，不要包含其他元素。以下是我的要求：

1. 整体大纲应该有引言,多个循序渐进的章节和总结，但不需要具体内容。
2. 大纲需要递归地包含多个标题，使用更小一级的标题代替无序列表和有序列表。
3. 标题的层次结构应清晰，让我能够方便地进行递归。

请注意，大纲中不需要包含除标题以外的任何元素。谢谢"""
        return self.GptChain.predict(text)

    def predict_outline_v3(self, title, title_requirement):
        text = f"""我选择第{title}个标题，为我生成一个只包含标题的有效大纲。请确保大纲的每一部分都是以 Markdown 格式的标题 (#, ##, ###, ####) 组成，不要包含其他元素。以下是我的要求：

1. 整体大纲应该有引言,多个循序渐进的章节和总结，但不需要具体内容。
2. 大纲需要递归地包含多个标题，使用更小一级的标题代替无序列表和有序列表。
3. 标题的层次结构应清晰，让我能够方便地进行递归。

请注意，大纲中不需要包含除标题以外的任何元素。谢谢"""
        return self.GptChain.predict(text)


class GenBody(Gen):
    def __init__(self, session_id):
        super().__init__(session_id)

    def predict_body(self, fix_outline=None, requirement=None):
        if fix_outline == "" or fix_outline == None:
            text = f"""请根据大纲填充markdowm文本,我希望你同样以markdown的格式返回,并且请遵循以下要求:
            1.不要丢失原有的大纲markdown信息;
            2.你需要根据每一个标题的信息扩写新增一个或者多个段落,每个段落必须使用<p></p>标签包围;
            3.对正文来说，要求{requirement}
            4.你需要把生成的段落放在正确的位置;
            """
        else:
            text = f"""我对大纲进行了如下修改,这是修改后的大纲:
            ```{fix_outline}``` 
            请根据大纲生成的PPT文本的正文内容,我希望你同样以markdown的格式返回,并且请遵循以下要求:
            1.不要丢失原有的大纲markdown信息和格式;
            2.你需要根据每一个标题的信息,结合上下文在标题的下一行新增一个或者多个段落,每个段落必须使用<p></p>标签包围;
            3.对正文来说，要求{requirement}
            4.你需要把生成的段落放在正确的位置;
            """
        return self.GptChain.predict(text)

    def predict_body_v3(self):
        #获取历史信息
        markdown_outline = self.GptChain.get_history_last()
        gen = TreeGen(markdown_outline)
        return gen.output()

if __name__ == '__main__':
    session_id = str(uuid.uuid4())

    title = GenTitle(session_id)
    title.predict_title("新人如何直播")

    outline = GenOutline(session_id)
    outline.predict_outline("1")

    body = GenBody(session_id)
    md = body.predict_body("")

    Tree2PPT(md)
    # csv = GenCsv(session_id)
    # csv.predict_csv()

# 将一个问题拆分成多个子问题解决,可以大大提高AI对问题的理解,从而提高程序的速度和准确性
