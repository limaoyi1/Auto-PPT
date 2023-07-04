import warnings

import openai

warnings.filterwarnings('ignore')

import codecs
import configparser

config = configparser.ConfigParser()
# 指定编码为 UTF-8
config.read_file(codecs.open('config.ini', 'r', 'utf-8-sig'))
Real_File = config.get('Credentials', 'Real_File')
if Real_File == "Config.ini":
    openai.api_base = config.get('Credentials', 'OPENAI_BASE_URL')
    openai.api_key = config.get('Credentials', 'OPENAI_API_KEY')
    pass
else:
    config.read_file(codecs.open(Real_File, 'r', 'utf-8-sig'))
    openai.api_base = config.get('Credentials', 'OPENAI_BASE_URL')
    openai.api_key = config.get('Credentials', 'OPENAI_API_KEY')


def get_gpt_data(title):
    # llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", max_tokens=10000)
    if title is None or title == "":
        raise ValueError("主题不能为空")
    # v1
    # text = "生成一份关于" + title + "的PPT的文本内容。要求有层次的大纲,300字以上,含有3级目录。以csv的格式返回,方便让我直接将字符串保存为 CSV 文件。必须返回表头,标题前不要产生多余的空格" \
    #                                   "csv有3列:'标题标识'，'标题文本'，'详细说明'。标题标识作为单独的一列数字(例如1.1.1)表示标题之间的层级关系,标题文本作为一列单独保存标题文本内容,详细说明作为单独的一列。" \
    #                                   "标题如果没有子标题或者是最小一级的标题，详细说明就必须要被生成。" \
    #                                   "标题文本不能为空。" \
    #                                   "如果详细说明为空，需要考虑csv的格式问题（例如: 1.1,[标题名称], ）保留逗号。" \
    #                                   "注意每一行结尾不要生成多余的英文逗号','，文本中的生成的','用'，'代替，详细内容以句号结尾。（例如: 1.1,[标题名称], [详细内容]）不需要保留逗号。"\
    #                                   "如果标题文本,详细说明字段中包含逗号，分隔符或换行符等特殊字符，需要使用引号将字段内容括起来。一般来说，使用单引号（'）进行包裹" \
    #                                   "我清晰地明白我请求的结果,不能返回csv之外的其他内容。返回的所有内容一定要需要满足csv的格式要求。"
    # v2.5
    # text = "返回一份csv内容格式的文本。这份csv有4个Column：'index','title','content','keyword'。'index'表示'title'之间的关系。" \
    #        "csv的内容是以```{" + title + "}```为主题的PPT文本内容，'index'是标题的等级，'title'是标题的内容，'content'是该标题的正文内容。'keyword'是总结后的一个或者多个关键英语单词,使用'&'进行拼接。" \
    #        "PPT至少有3级目录，PPT的幻灯片数量大于8张。" \
    #        "'index'的第一级是PPT的主题的索引，例如：\n1,'如何实现财富自由','掌握正确的理财观念和方法，迈向财富自由的道路。','wealth&freedom'\n" \
    #        "'index'的第二级是每一张幻灯片的主题的索引，例如：\n1.1,'正确的理财观念','正确的理财观念应该是：不把所有的蛋放在一个篮子里。正确的理财观念是基于健康的金融管理原则，旨在实现长期的财务稳定和增长。以下是一些正确的理财观念：','risk&management'\n" \
    #        "'index'的第三级是幻灯片的每一个重点的索引，例如：\n1.1.1,'学习和提高金融知识','了解基本的金融知识，包括投资、税务、财务规划等方面的知识。持续学习和更新知识，以做出明智的理财决策。','diversified investment'\n" \
    #        "正文内容'content'尽可能详细和具体" \
    #        "每一个幻灯片需要3个以上的重点。" \
    #        "cell中如果需要换行使用\\n代替，如果需要使用','使用'，'代替。用于分隔字段的单字符字符串，默认为','。" \
    #        "不需要返回csv的文本以外的任何内容，方便我使用程序直接将返回的字符串正确的保存为 CSV 文件。" \
    #        "注意不要生成多余的','导致pandas.errors.ParserError" \
    #        "第一行必须是：'index','title','content','keyword'"
    # v3.5
    text = f"""
           返回一份csv内容格式的PPT文本。遵循以下的要求：
           1.csv的内容是以```{title}```为主题的PPT文本内容。
           2.这份csv有4个Column：'index','title','content','keyword'。'index'表示'title'之间的关系。'index'是标题的等级，'title'是标题的内容，'content'是该标题的正文内容。'keyword'是总结后的一个或者多个关键英语单词,使用'&'进行拼接。'title','content'的内容使用中文回答。'keyword'的内容用英文回答。
           3.完成以```{title}```为主题的PPT时，你需要将根据主题生成为5个以上个详细的章节。每个章节有3张以上的幻灯片。你需要根据每个幻灯片内容的总结生成至少3个重点，重点内容尽可能详细和具体。
                例如：
                   0,"[PPT的主题]","[PPT的副标题]","[主题的关键词]"
                   1,"[PPT的章节1]","[章节1的介绍]","[章节1的关键词]"
                   1.1,"[幻灯片1.1的标题]","[幻灯片1.1内容的总结]","[关键词1.1]"
                   1.1.1,"[重点1的标题]","[重点1的详细内容]","[关键词1]"
                   1.1.2,"[重点2的标题]","[重点2的详细内容]","[关键词2]"
                   1.1.2,"[重点3的标题]","[重点3的详细内容]","[关键词3]" 
                   ...            #注释 提问需要省略的内容，生成的内容不能使用”...“省略
                   1.10,"[幻灯片1.10的标题]","[幻灯片1.10内容的总结]","[关键词1.10]"
                   2,"[PPT的章节2]","[章节2的副标题]","[章节2的关键词]"
                   2.1,"[幻灯片1的标题]","[幻灯片1内容的总结]","[关键词1]"
                   ...
                   5,"[PPT的章节5]","[章节5的副标题]","[章节5的关键词]"
                   ...      
           4.重点内容尽可能详细和具体，你需要使用8个以上的句子描述。如果需要换行使用\\n代替，如果需要使用','使用'，'代替。用于分隔字段的单字符字符串，默认为','。
           5.不需要返回csv的文本以外的任何内容，方便我使用程序直接将返回的字符串正确的保存为 CSV 文件。
           6.注意不要生成多余的','导致pandas.errors.ParserError。
           7.第一行必须是：'index','title','content','keyword'。不要产生多余的空格。
           8.'title','content'的内容使用中文回答。'keyword'是总结后的一个或者多个关键英语单词,使用'&'进行拼接。
           9.如果不能按照要求生成文本，请告诉我原因。
"""
    # english demo
    # v4.5.1
    textV4 = f"""
Return a PPT text in csv content format. Follow the requirements below:
        a. The content of csv is the PPT text content with the theme of ```{title}```.
        b. This csv has 4 Columns: 'index', 'title', 'content', 'keyword'. 'index' represents the relationship between 'title'. 'index' is the rank of the title, 'title' is the content of the title, and 'content' is the body content of the title. 'keyword' is one or more key English words after the summary, use '&' to splice. The contents of 'title' and 'content' are answered in Chinese. The content of 'keyword' is answered in English.
        c. When completing the PPT with the theme of ```{title}```, you need to generate more than 5 detailed chapters according to the theme. Each chapter has 3+ slides. You need to generate at least 3 subtitles based on the summary of the content of each slide, and the subtitles should be as detailed and specific as possible.You need to provide a detailed introduction based on the subheading, at least 4 sentences or more, and place the content in content.
             this is my tip for you:
                "index","title","content","keyword"
                0,"[Theme of the PPT]","[The subtitle of the PPT]","[Keywords of the topic]"
                1,"[Chapter 1 of PPT]","[Introduction of Chapter 1]","[Keywords of Chapter 1]"
                1.1,"[Title Text of Slide 1.1]","[Summary of Slide 1.1 Content]","[Keywords 1.1]"
                1.1.1,"[subtitle 1]","[Introduce according to the subtitle 1]","[Keyword 1]"
                1.1.2,"[subtitle 2]","[Introduce according to the subtitle 2]","[Keyword 2]"
                1.1.3,"[subtitle 3]","[Introduce according to the subtitle 3]","[Keyword 3]"            
                ... # Annotate the content that needs to be omitted for questioning, and the generated content cannot be used Omit
                1.3,"[Title Text of Slide 1.3]","[Summary of Slide 1.3 Content]","[Keywords 1.3]"
                1.3.1,"[subtitle 1]","[Introduce according to the subtitle 1]","[Keyword 1]"
                1.3.2,"[subtitle 2]","[Introduce according to the subtitle 2]","[Keyword 2]"
                1.3.3,"[subtitle 3]","[Introduce according to the subtitle 3]","[Keyword 3]"   
                ...
                5,"[Chapter 5 of PPT]","[Subtitle of Chapter 5]","[Keywords of Chapter 5]"
                5.1,"[Title Text of Slide 3]","[Summary of Slide 3 Content]","[Keyword 3]"
                5.1.1,"[subtitle 1]","[Introduce according to the subtitle 1]","[Keyword 1]"
                5.1.2,"[subtitle 2]","[Introduce according to the subtitle 2]","[Keyword 2]"
                5.1.4,"[subtitle 3]","[Introduce according to the subtitle 3]","[Keyword 3]"   
                ...
                5.3,"[Title Text of Slide 5.3]","[Summary of Slide 5.3 Content]","[Keywords 5.3]"
                5.3.1,"[subtitle 1]","[Introduce according to the subtitle 1]","[Keyword 1]"
                5.3.2,"[subtitle 2]","[Introduce according to the subtitle 2]","[Keyword 2]"
                5.3.4,"[subtitle 3]","[Introduce according to the subtitle 3]","[Keyword 3]"
            For example,
                1.1.1,"Python的起源","Python是由Guido van Rossum于20世纪90年代初创建的编程语言。它的名字来自于Guido van Rossum喜欢的电视剧《Monty Python's Flying Circus》。Python的目标是成为一种简单易学、可读性强的语言。它在开源社区中得到了广泛的认可和应用，成为了Web开发、科学计算、人工智能等领域的首选语言之一。","origin"
        d. The key content should be as detailed and specific as possible, and you need to use more than 5 sentences to describe it. If you need to change the line, use \\n instead, if you need to use ',', use ',' instead. Single-character string used to separate fields, defaults to ','.
        e. There is no need to return anything other than the text of the csv, so that I can use the program to directly save the returned string as a CSV file correctly.
        f. Be careful not to generate redundant ',' causing pandas.errors.ParserError.
        g. The csv's first line must be:"index","title","content","keyword". Do not generate extra spaces.
        h. The contents of 'title' and 'content' should be answered in Chinese. 'keyword' is one or more key English words after the summary, use '&' to splice.
        i. If the text cannot be generated as required, please tell me the reason.
"""
    # text1 = llm(textV4)
    # 非流式传输
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k", messages=[{"role": "user", "content": textV4}])
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


def get_gpt_expand(titles, contents):
    llm = OpenAI(temperature=0.9, model_name="gpt-3.5-turbo", max_tokens=3300)
    text = "帮助我补充一份csv内容格式的文本。这份csv有3个Column:title,content,expand。" \
           "需要你通过标题 'tilte' 和主旨 'content' 生成 'expand'。 要求内容丰富,生成至少3个自然段落。" \
           "直接返回修改后的csv文本，不需要返回csv的文本以外的任何内容，方便我使用程序直接将返回的字符串正确的保存为 CSV 文件。" \
           "cell中如果需要换行使用\\n代替，如果需要使用','使用'，'代替。用于分隔字段的单字符字符串，默认为','。" \
           "以下是我给你的问题的csv文本:\n" \
           "title,content,expand\n"
    csv = ""
    for i in range(len(titles)):
        csv = csv + titles[i] + "," + contents[i] + "\n"
    text = text + csv
    print(text)
    return llm(text)


# test 测试
if __name__ == '__main__':
    text1 = get_gpt_data("述职报告")
    # print(text1)
    # df = pd.read_csv("1.csv")
    # expand = get_gpt_expand(df["title"], df["content"])
    # print("================================================")
    # print(expand)
