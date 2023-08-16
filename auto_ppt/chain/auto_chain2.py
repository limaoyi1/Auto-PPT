# -*- coding: utf-8 -*-
# @Time    : 2023/8/16 14:14
# @Author  : limaoyi
# @File    : auto_chain2.py
# @Software: PyCharm
# @GitHub  : https://github.com/limaoyi1/GPT-prompt
import os
from collections import deque
from typing import Dict, List, Optional, Any

from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import BaseLLM
from langchain.vectorstores.base import VectorStore
from pydantic import BaseModel, Field
from langchain.chains.base import Chain
from langchain_experimental.autonomous_agents import BabyAGI

from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore

# Define your embedding model
embeddings_model = OpenAIEmbeddings()
# Initialize the vectorstore as empty
import faiss

embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

OBJECTIVE = "写一篇<<开源项目管理之道>>的markdown文章"

llm = OpenAI(temperature=0)

# Logging of LLMChains
verbose = False
# If None, will keep on going forever
max_iterations: Optional[int] = 10
baby_agi = BabyAGI.from_llm(
    llm=llm, vectorstore=vectorstore, verbose=verbose, max_iterations=max_iterations
)

agi = baby_agi({"objective": OBJECTIVE})

print(agi)