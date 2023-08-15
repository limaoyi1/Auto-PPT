# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 11:12
# @Author  : limaoyi
# @File    : auto_chain.py
# @Software: PyCharm
# @GitHub  : https://github.com/limaoyi1/GPT-prompt
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.experimental import load_chat_planner, load_agent_executor, PlanAndExecute
from langchain.memory import RedisChatMessageHistory, ConversationBufferMemory
from langchain.prompts import PromptTemplate

from readconfig.myconfig import MyConfig

config = MyConfig()
session_id = "123456"

# 顺序标题链
# This is an LLMChain to write a synopsis given a title of a play.
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=.7, openai_api_key=config.OPENAI_API_KEY,
                 openai_api_base=config.OPENAI_BASE_URL)

planner = load_chat_planner(llm)

executor = load_agent_executor(llm, verbose=True)

agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)

run = agent.run("完成'java的魅力'的文章的大纲")

print(run)

