# Build a sample vectorDB
from langchain.document_loaders import WebBaseLoader
# from langchain.document_loaders import WebBaseLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from readconfig.myconfig import MyConfig

config = MyConfig()

# Load blog post
loader = WebBaseLoader("http://www.limaoyi.top/2023/06/27/Scrapy-%E5%85%A5%E9%97%A8%E6%8C%87%E5%8D%97-%E4%B8%80-%E5%AE%89%E8%A3%85%E4%B8%8E%E7%AE%80%E5%8D%95%E4%BD%BF%E7%94%A8/")
data = loader.load()

# Split
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
splits = text_splitter.split_documents(data)

# VectorDB
embedding = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
vectordb = Chroma.from_documents(documents=splits, embedding=embedding)

from langchain.chat_models import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
question="What are the scrapy?"
llm = ChatOpenAI(temperature=0,openai_api_key=config.OPENAI_API_KEY)
retriever_from_llm = MultiQueryRetriever.from_llm(retriever=vectordb.as_retriever(), llm=llm)

# Set logging for the queries
import logging
logging.basicConfig()
logging.getLogger('langchain.retrievers.multi_query').setLevel(logging.INFO)

unique_docs = retriever_from_llm.get_relevant_documents(query=question)
print(unique_docs)
len(unique_docs)

from typing import List
from langchain import LLMChain
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser


# Output parser will split the LLM result into a list of queries
class LineList(BaseModel):
    # "lines" is the key (attribute name) of the parsed output
    lines: List[str] = Field(description="Lines of text")


class LineListOutputParser(PydanticOutputParser):
    def __init__(self) -> None:
        super().__init__(pydantic_object=LineList)

    def parse(self, text: str) -> LineList:
        lines = text.strip().split("\n")
        return LineList(lines=lines)


output_parser = LineListOutputParser()

QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant. Your task is to generate five 
    different versions of the given user question to retrieve relevant documents from a vector 
    database. By generating multiple perspectives on the user question, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search. 
    Provide these alternative questions seperated by newlines.
    Original question: {question}""",
)
#  你是一名AI语言模型助手。你的任务是生成五个
#     给定用户问题的不同版本，用于从向量中检索相关文档
#     数据库。通过对用户问题产生多种观点，您的目标是帮助
#     用户克服了基于距离的相似性搜索的一些限制。
#     提供这些替代问题，并用换行符分隔。
#     原始问题：{问题}
llm = ChatOpenAI(temperature=0,openai_api_key=config.OPENAI_API_KEY)

# Chain
llm_chain = LLMChain(llm=llm, prompt=QUERY_PROMPT, output_parser=output_parser)

# Other inputs
# question = "What are the approaches to Task Decomposition?"

# Run
retriever = MultiQueryRetriever(retriever=vectordb.as_retriever(),
                                llm_chain=llm_chain,
                                parser_key="lines")  # "lines" is the key (attribute name) of the parsed output

# Results
unique_docs = retriever.get_relevant_documents(query="What does the course say about regression?")
for e in unique_docs:
    print(e)
len(unique_docs)