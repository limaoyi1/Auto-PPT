# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 11:12
# @Author  : limaoyi
# @File    : auto_chain.py
# @Software: PyCharm
# @GitHub  : https://github.com/limaoyi1/GPT-prompt

from collections import deque
from typing import Dict, List, Optional, Any

import torch as torch
from langchain import LLMChain, PromptTemplate, FAISS, InMemoryDocstore
from langchain.chains.base import Chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import BaseLLM
from langchain.vectorstores.base import VectorStore
from pydantic import BaseModel, Field

from readconfig.myconfig import MyConfig

config = MyConfig()

# 顺序标题链
# This is an LLMChain to write a synopsis given a title of a play.
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=.7, openai_api_key=config.OPENAI_API_KEY,
                 openai_api_base=config.OPENAI_BASE_URL)

# Define your embedding model

embeddings_model = OpenAIEmbeddings()

# Initialize the vectorstore as empty
import faiss

embedding_model_dict = {
    # "ernie-base": "models/ernie-3.0-base-zh",
    "text2vec-base": "shibing624/text2vec-base-chinese"
    # "text2vec-large": "models/text2vec-large-chinese",
    # "sentence-transformers-v2": "models/sentence-transformers-v2"
}

EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

# embeddings_model = HuggingFaceEmbeddings(model_name=embedding_model_dict['text2vec-base'], model_kwargs={'device': EMBEDDING_DEVICE})

embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

# 放弃使用 Chroma 安装太麻烦了
# pip install faiss-cpu
i = 0
j = 0
k = 0


# 任务创建链，用于选择要添加到列表中的新任务
class TaskCreationChain(LLMChain):
    """Chain to generates tasks."""

    @classmethod
    def from_llm(cls, llm: BaseLLM, verbose: bool = True, i1=None, i=i) -> LLMChain:
        """Get the response parser."""
        task_creation_template = (
            "你是一个任务创建人工智能，使用执行代理的结果"
            "创建具有以下目标的新任务：{objective}，"
            "最后完成的任务的结果是：{result}。"
            "此结果基于此任务描述：{task_description}。"
            "这些是未完成的任务：{incomplete_tasks}。"
            "根据结果，创建要完成的新任务"
            "由人工智能系统完成，不会与未完成的任务重叠。"
            "以数组形式返回任务。"
        )
        prompt = PromptTemplate(
            template=task_creation_template,
            input_variables=[
                "result",
                "task_description",
                "incomplete_tasks",
                "objective",
            ],
        )
        i += 1
        return cls(prompt=prompt, llm=llm, verbose=verbose)


# 任务优先级链，用于重新确定任务的优先级
class TaskPrioritizationChain(LLMChain):
    """Chain to prioritize tasks."""

    @classmethod
    def from_llm(cls, llm: BaseLLM, verbose: bool = True, j=j) -> LLMChain:
        """Get the response parser."""
        task_prioritization_template = (
            "你是一个任务优先级人工智能，负责清理格式并重新确定优先级"
            "以下任务：{task_names}。"
            "考虑您团队的最终目标：{objective}。"
            "不要删除任何任务。以编号列表的形式返回结果，例如："
            "1. First task"
            "2. Second task"
            "以编号 {next_task_id} 开始任务列表。"
        )
        prompt = PromptTemplate(
            template=task_prioritization_template,
            input_variables=["task_names", "next_task_id", "objective"],
        )
        j += 1
        return cls(prompt=prompt, llm=llm, verbose=verbose)


# 执行任务的执行链
class ExecutionChain(LLMChain):
    """Chain to execute tasks."""

    @classmethod
    def from_llm(cls, llm: BaseLLM, verbose: bool = True, k=k) -> LLMChain:
        """Get the response parser."""
        execution_template = (
            "你是一个人工智能，根据以下目标执行一项任务：{objective}。"
            "考虑到这些之前完成的任务：{context}。"
            "您的任务：{task}。"
            "回复："
        )
        prompt = PromptTemplate(
            template=execution_template,
            input_variables=["objective", "context", "task"],
        )
        k += 1
        return cls(prompt=prompt, llm=llm, verbose=verbose)


def get_next_task(
        task_creation_chain: LLMChain,
        result: Dict,
        task_description: str,
        task_list: List[str],
        objective: str,
) -> List[Dict]:
    """Get the next task."""
    incomplete_tasks = ", ".join(task_list)
    response = task_creation_chain.run(
        result=result,
        task_description=task_description,
        incomplete_tasks=incomplete_tasks,
        objective=objective,
    )
    new_tasks = response.split("\n")
    return [{"task_name": task_name} for task_name in new_tasks if task_name.strip()]


def prioritize_tasks(
        task_prioritization_chain: LLMChain,
        this_task_id: int,
        task_list: List[Dict],
        objective: str,
) -> List[Dict]:
    """Prioritize tasks."""
    task_names = [t["task_name"] for t in task_list]
    next_task_id = int(this_task_id) + 1
    response = task_prioritization_chain.run(
        task_names=task_names, next_task_id=next_task_id, objective=objective
    )
    new_tasks = response.split("\n")
    prioritized_task_list = []
    for task_string in new_tasks:
        if not task_string.strip():
            continue
        task_parts = task_string.strip().split(".", 1)
        if len(task_parts) == 2:
            task_id = task_parts[0].strip()
            task_name = task_parts[1].strip()
            prioritized_task_list.append({"task_id": task_id, "task_name": task_name})
    return prioritized_task_list


def _get_top_tasks(vectorstore, query: str, k: int) -> List[str]:
    """Get the top k tasks based on the query."""
    results = vectorstore.similarity_search_with_score(query, k=k)
    if not results:
        return []
    sorted_results, _ = zip(*sorted(results, key=lambda x: x[1], reverse=True))
    return [str(item.metadata["task"]) for item in sorted_results]


def execute_task(
        vectorstore, execution_chain: LLMChain, objective: str, task: str, k: int = 5
) -> str:
    """Execute a task."""
    context = _get_top_tasks(vectorstore, query=objective, k=k)
    return execution_chain.run(objective=objective, context=context, task=task)


class BabyAGI(Chain, BaseModel):
    """Controller model for the BabyAGI agent."""

    task_list: deque = Field(default_factory=deque)
    task_creation_chain: TaskCreationChain = Field(...)
    task_prioritization_chain: TaskPrioritizationChain = Field(...)
    execution_chain: ExecutionChain = Field(...)
    task_id_counter: int = Field(1)
    vectorstore: VectorStore = Field(init=False)
    max_iterations: Optional[int] = None

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def add_task(self, task: Dict):
        self.task_list.append(task)

    def print_task_list(self):
        print("\033[95m\033[1m" + "\n*****TASK LIST*****\n" + "\033[0m\033[0m")
        for t in self.task_list:
            print(str(t["task_id"]) + ": " + t["task_name"])

    def print_next_task(self, task: Dict):
        print("\033[92m\033[1m" + "\n*****NEXT TASK*****\n" + "\033[0m\033[0m")
        print(str(task["task_id"]) + ": " + task["task_name"])

    def print_task_result(self, result: str):
        print("\033[93m\033[1m" + "\n*****TASK RESULT*****\n" + "\033[0m\033[0m")
        print(result)

    @property
    def input_keys(self) -> List[str]:
        return ["objective"]

    @property
    def output_keys(self) -> List[str]:
        return []

    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Run the agent."""
        objective = inputs["objective"]
        first_task = inputs.get("first_task", "Make a todo list")
        self.add_task({"task_id": 1, "task_name": first_task})
        num_iters = 0
        while True:
            if self.task_list:
                self.print_task_list()

                # Step 1: Pull the first task
                task = self.task_list.popleft()
                self.print_next_task(task)

                # Step 2: Execute the task
                result = execute_task(
                    self.vectorstore, self.execution_chain, objective, task["task_name"]
                )
                this_task_id = int(task["task_id"])
                self.print_task_result(result)

                # Step 3: Store the result in Pinecone
                result_id = f"result_{task['task_id']}_{num_iters}"
                self.vectorstore.add_texts(
                    texts=[result],
                    metadatas=[{"task": task["task_name"]}],
                    ids=[result_id],
                )

                # Step 4: Create new tasks and reprioritize task list
                new_tasks = get_next_task(
                    self.task_creation_chain,
                    result,
                    task["task_name"],
                    [t["task_name"] for t in self.task_list],
                    objective,
                )
                for new_task in new_tasks:
                    self.task_id_counter += 1
                    new_task.update({"task_id": self.task_id_counter})
                    self.add_task(new_task)
                self.task_list = deque(
                    prioritize_tasks(
                        self.task_prioritization_chain,
                        this_task_id,
                        list(self.task_list),
                        objective,
                    )
                )
            num_iters += 1
            if self.max_iterations is not None and num_iters == self.max_iterations:
                print(
                    "\033[91m\033[1m" + "\n*****TASK ENDING*****\n" + "\033[0m\033[0m"
                )
                break
        return {}

    @classmethod
    def from_llm(
            cls, llm: BaseLLM, vectorstore: VectorStore, verbose: bool = False, **kwargs
    ) -> "BabyAGI":
        """Initialize the BabyAGI Controller."""
        task_creation_chain = TaskCreationChain.from_llm(llm, verbose=verbose)
        task_prioritization_chain = TaskPrioritizationChain.from_llm(
            llm, verbose=verbose
        )
        execution_chain = ExecutionChain.from_llm(llm, verbose=verbose)
        return cls(
            task_creation_chain=task_creation_chain,
            task_prioritization_chain=task_prioritization_chain,
            execution_chain=execution_chain,
            vectorstore=vectorstore,
            **kwargs,
        )


if __name__ == "__main__":
    OBJECTIVE = "完成一篇标题为<<开源项目管理之道>>的markdown文章"
    # Logging of LLMChains
    verbose = False
    # If None, will keep on going forever
    max_iterations: Optional[int] = 20
    baby_agi = BabyAGI.from_llm(
        llm=llm, vectorstore=vectorstore, verbose=verbose, max_iterations=max_iterations
    )


    baby_agi({"objective": OBJECTIVE})
    print("任务创建链,优先链,执行链的次数")
    print(i)
    print(j)
    print(k)
