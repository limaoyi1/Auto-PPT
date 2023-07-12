import os

import pinecone

from readconfig.myconfig import MyConfig

config = MyConfig()
openai_api_key = config.OPENAI_API_KEY

from langchain.schema import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
# create new index
pinecone.create_index(name="langchain-self-retriever-demo", dimension=1536)
