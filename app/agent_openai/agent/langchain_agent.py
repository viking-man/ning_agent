from langchain.agents import load_tools, initialize_agent, Tool, AgentExecutor, AgentType
from langchain.chat_models import ChatOpenAI
from app.type import ChatGPTModel
from app.open_ai.openai_config import OPENAI_API_KEY
from app.agent_openai.tools.web_search import GoogleSearch
from app.agent_openai.tools.rag_search import RagSearch
from typing import List, Tuple, Any, Union, Optional, Type
import logging


class LangchainAgent:
    tool_names: str = ""
    agent_executor: any
    tools: List[Tool]
    llm_chain: any

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

        self.agent_executor = initialize_agent(
            tools,
            llm,
            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            verbose=True)

    def agent_query(self, input: str = ""):
        logging.info(f"执行Agent查询,输入{input}")
        result = self.agent_executor.run(input=input)
        logging.info(f"执行Agent查询,输入{input}，输出{result}")
        return result


if __name__ == "__main__":
    import langchain
    langchain.debug = True
    print(OPENAI_API_KEY)
    agent = LangchainAgent()
    result = agent.agent_query("历史上中国最早的朝代")
    print(result)
