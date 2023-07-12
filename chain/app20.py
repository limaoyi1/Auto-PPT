# 索引工具
import os

os.environ["OPENAI_API_KEY"] = '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'
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter


def get_answer():
    loader = TextLoader("./data/test3.txt", encoding="utf-8")
    index = VectorstoreIndexCreator(text_splitter=CharacterTextSplitter(chunk_size=500, chunk_overlap=0)).from_loaders(
        [loader])
    question = "总统说了什么"
    print(index.query(question))


get_answer()
