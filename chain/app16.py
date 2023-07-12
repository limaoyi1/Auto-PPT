import os

import openai
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

os.environ["OPENAI_API_KEY"] = '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'


def search_text():
    loader = DirectoryLoader('C:/Users/thgy/Desktop/文章数据/学习培训演讲材料', glob='**/*.docx')
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=0)
    split_docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(split_docs, embeddings)
    return docsearch


def write_doc():
    topic = "培训班"
    docsearch = search_text()
    docs = docsearch.similarity_search(topic, k=1)
    doc = docs[0]
    page_content = doc.page_content
    prompt = PromptTemplate(
        input_variables=["topic", "context"],
        template="使用下面的上下文写一篇关于下面主题的2000字博客文章: Context: {context} Topic: {topic}",
    )
    llm = ChatOpenAI(temperature=0.9, model_name="gpt-3.5-turbo", max_tokens=3700)
    chain = LLMChain(llm=llm, prompt=prompt)

    print(chain.run(topic=topic, context=page_content))


write_doc()
