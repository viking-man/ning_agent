from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain import PromptTemplate, LLMChain
from ..tools.web_search import GoogleSearch
from ..tools.rag_search import RagSearch
from langchain.agents import BaseSingleActionAgent, AgentOutputParser, LLMSingleActionAgent, AgentExecutor
from typing import List, Tuple, Any, Union, Optional, Type
from langchain.schema import AgentAction, AgentFinish
from langchain.prompts import StringPromptTemplate
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.chat_models import ChatOpenAI
from app.type import ChatGPTModel
from app.agent_openai.agent.agent_template import *
import re
from app.open_ai.openai_config import OPENAI_API_KEY


class CustomPromptTemplate(StringPromptTemplate):
    template: str
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        intermediate_steps = kwargs.pop("intermediate_steps")
        # 没有互联网查询信息
        if len(intermediate_steps) == 0:
            background_infomation = "\n"
            template = router_tempalte

        # 返回了背景信息
        else:
            # 根据 intermediate_steps 中的 AgentAction 拼装 background_infomation
            background_infomation = "\n\n你还有这些已知信息作为参考：\n\n"
            action, observation = intermediate_steps[0]
            background_infomation += f"{observation}\n"
            if "Default" or "Answer" == action.tool:
                template = generate_template
            else:
                # todo 先默认返回空，后续再看
                return ""

        kwargs["background_content"] = background_infomation
        kwargs["related_content"] = background_infomation
        return template.format(**kwargs)


class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # 正则表达式模式，用于匹配所需的格式
        pattern = r"(Answer|Music|Video|Painting|Default)\('([^']*)'\)"

        # 使用 re.match 检查字符串是否与模式匹配
        match = re.match(pattern, llm_output)

        # 如果 llm 没有返回 GoogleSearch() 则认为直接结束指令
        if not match:
            return AgentFinish(
                return_values={"output": llm_output.strip()},
                log=llm_output,
            )
        # 否则的话都认为需要调用 Tool
        else:
            action = match.group(1).strip()
            action_input = match.group(2).strip()
            return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)


class NingAgent:
    tool_names: str = ""
    agent_executor: any
    tools: List[Tool]
    llm_chain: any

    def query(self, query: str = "", chat_history: str = ""):
        # tool_name = self.tool_name
        result = self.agent_executor.run(chat_history=chat_history, input=query, tool_name="")
        return result

    def __init__(self, **kwargs):
        llm = ChatOpenAI(temperature=0, model=ChatGPTModel.GPT3.value, openai_api_key=OPENAI_API_KEY)
        tools = [
            Tool.from_function(
                func=GoogleSearch.web_search,
                name="Default",
                description="Utilize the default web search tool to investigate the user's query, focusing on the most recent web pages that provide explanations. The findings should be used as reference material for the large model."
            ),
            Tool.from_function(
                func=RagSearch.rag_search,
                name="Answer",
                description="Utilize the default web search tool to investigate the user's query, focusing on the most recent web pages that provide explanations. The findings should be used as reference material for the large model."
            ),
        ]
        self.tools = tools
        tool_names = [tool.name for tool in tools]
        output_parser = CustomOutputParser()
        prompt = CustomPromptTemplate(template="",
                                      tools=tools,
                                      input_variables=["chat_history", "input", "intermediate_steps"])

        llm_chain = LLMChain(llm=llm, prompt=prompt)
        self.llm_chain = llm_chain

        agent = LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=output_parser,
            stop=["\nObservation:"],
            allowed_tools=tool_names
        )

        agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
        self.agent_executor = agent_executor
