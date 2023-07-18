import uuid

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
                                 redis_url=self.config.REDIS_URL)


# ----------------------------------------------------------------
# 生成标题
class GenTitle(Gen):
    def __init__(self, session_id):
        super().__init__(session_id)

    def predict_title(self, query):
        text = f"""我希望你帮助我以```{query}```为题生成3个PPT的标题.要求能吸引人的注意.
        """
        return self.GptChain.predict(text)

    def predict_title_v2(self, form, role, title1, topic_num=1):
        text = f"""
                我希望你作为```{role}```，以```{title1}```为主题生成{topic_num}个```{form}```PPT标题，要求能吸引人的注意。
                以下是返回的一些要求：
                1.【The response should be a list of {topic_num} items separated by \"\n\" (例如: 香蕉\n天气\n说明)】
            """
        return self.GptChain.predict(text)


class GenOutline(Gen):
    def __init__(self, session_id):
        super().__init__(session_id)

    def predict_outline(self, query):
        text = f"""我选择的标题是第```{query}```个标题,我希望你用markdown的格式生成一个只有标题的大纲,并且请遵循以下要求:
        1.如果要创建标题，请在单词或短语前面添加井号 (#) 。# 的数量代表了标题的级别。
        2.不能使用无序或者有序列表,必须全部使用添加井号 (#)的方式表示大纲结构.
        3.第一级(#)表示大纲的标题,第二级(##)表示章节的标题,第三级(###)表示章节的重点.
        4.大纲的第一章是```{query}```的简介，最后一章是总结；
        """
        return self.GptChain.predict(text)

    def predict_outline_v2(self, title, title_requirement):
        text = f"""我希望你使用markdown的格式根据```{title}```生成一个只有标题的大纲，并且请遵循以下要求:
            1.如果要创建标题，请在单词或短语前面添加井号 (#) 。# 的数量代表了标题的级别。
            2.不能使用无序或者有序列表,必须全部使用添加井号 (#)的方式表示大纲结构.
            3.第一级(#)表示大纲的标题,第二级(##)表示章节的标题,第三级(###)表示章节的重点.
            4.对大纲来说，要求```{title_requirement}```
            5.大纲的第一章是```{title}```的简介，最后一章是总结；
        """
        return self.GptChain.predict(text)


class GenBody(Gen):
    def __init__(self, session_id):
        super().__init__(session_id)

    def predict_body(self, fix_outline = None, requirement = None):
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
