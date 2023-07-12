# 异步链
import asyncio
import os

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader

from readconfig.myconfig import MyConfig

os.environ["OPENAI_API_KEY"] = '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'
config = MyConfig()

# 分词 -> 存储至向量数据库 -> 获取数据集合
def search_text():
    loader = DirectoryLoader('C:/Users/thgy/Desktop/文章数据/学习培训演讲材料', glob='**/*.docx')
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=0)
    split_docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
    docsearch = Chroma.from_documents(split_docs, embeddings)
    return docsearch


# 执行链操作（搜素向量文章 -> gpt3.5 二次加工）
async def write_doc(chain, page_content, topic):
    return await chain.arun(topic=topic, context=page_content)


# 写文章，突破4096字数，受限于 gpt api 的tps限制，每分钟3次（充钱解决）
async def write_docs():
    topic = "培训班"
    docsearch = search_text()
    docs = docsearch.similarity_search(topic, k=10)
    prompt = PromptTemplate(
        input_variables=["topic", "context"],
        template="使用下面的上下文写一篇关于下面主题的2000字博客文章: Context: {context} Topic: {topic}"
    )
    llm = ChatOpenAI(temperature=0.9, model_name="gpt-3.5-turbo", max_tokens=3600,openai_api_key=config.OPENAI_API_KEY)
    chain = LLMChain(llm=llm, prompt=prompt)
    task_list = []
    for _ in docs:
        task = write_doc(chain, _.page_content, topic)
        task_list.append(task)
    results = await asyncio.gather(*task_list)
    text = ""
    for r in results:
        text = text + r
    print(text)


# langchain官方文档的asyncio.run(有时会报错 RuntimeError:Event loop is closed，是因为asyncio.run(会自动关团循环，并且调用ProactorBasePipeTransport. del 而报错，
# 把asyncio.run()改为asyncio.get_event_loop().run_until_complete(main())


# asyncio.run(write_docs())
asyncio.get_event_loop().run_until_complete(write_docs())
