# -*- coding: utf-8 -*-
# @Time    : 2023/8/16 14:14
# @Author  : limaoyi
# @File    : auto_chain2.py
# @Software: PyCharm
# @GitHub  : https://github.com/limaoyi1/GPT-prompt
from typing import Optional

from langchain import PromptTemplate
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_experimental.autonomous_agents import BabyAGI

from readconfig.myconfig import MyConfig

config = MyConfig()
# Define your embedding model
embeddings_model = OpenAIEmbeddings()
# Initialize the vectorstore as empty
import faiss

embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain import OpenAI, LLMChain


class MarkdownFaker:
    markdown_str: str

    def __init__(self, markdown_str=""):
        self.markdown_str = markdown_str

    def read(self,anyone):
        if(self.markdown_str == ""):
            return "没有写入任何信息"
        return self.markdown_str

    def edit(self, markdown_str):
        self.markdown_str = markdown_str


todo_prompt = PromptTemplate.from_template(
    "You are a planner who is an expert at coming up with a todo list for a given objective. Come up with a todo list for this objective: {objective}"
)
todo_chain = LLMChain(llm=OpenAI(temperature=0), prompt=todo_prompt)
markdown_faker = MarkdownFaker()
tools = [
    Tool(
        name="markdown-reader",
        func=markdown_faker.read,
        description="useful for when you need to read the markdown article you wrote yourself, do not pass in parameters",
    ),
    Tool(
        name="markdown-editor",
        func=markdown_faker.edit,
        description="useful for when you need to edit the markdown article you wrote yourself, you need to pass in the entire article as a str",
    ),
    Tool(
        name="TODO",
        func=todo_chain.run,
        description="useful for when you need to come up with todo lists. Input: an objective to create a todo list for. Output: a todo list for that objective. Please be very clear what the objective is!",
    ),
]

prefix = """You are an AI who performs one task based on the following objective: {objective}. Take into account these previously completed tasks: {context}."""
suffix = """Question: {task}
{agent_scratchpad}"""
prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["objective", "task", "context", "agent_scratchpad"],
)

llm = OpenAI(temperature=0, openai_api_key=config.OPENAI_API_KEY,
             openai_api_base=config.OPENAI_BASE_URL)
llm_chain = LLMChain(llm=llm, prompt=prompt)
tool_names = [tool.name for tool in tools]
agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True
)

OBJECTIVE = "帮我写一篇关于开源项目管理的文章"

# Logging of LLMChains
verbose = False
# If None, will keep on going forever
max_iterations: Optional[int] = 10
baby_agi = BabyAGI.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    task_execution_chain=agent_executor,
    verbose=verbose,
    max_iterations=max_iterations,
)

baby_agi({"objective": OBJECTIVE})

print("=======================================")
print(markdown_faker.read())