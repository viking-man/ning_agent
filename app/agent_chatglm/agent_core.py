from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain import PromptTemplate, LLMChain
from app.agent_chatglm.agent_web_search import GoogleSearch
from app.agent_chatglm.agent_template import agent_template
from langchain.agents import BaseSingleActionAgent, AgentOutputParser, LLMSingleActionAgent, AgentExecutor
from typing import List, Tuple, Any, Union, Optional, Type
from langchain.schema import AgentAction, AgentFinish
from langchain.prompts import StringPromptTemplate
from langchain.callbacks.manager import CallbackManagerForToolRun
from app.agent_chatglm.agent_llm import CustomLLM
import re
from app.agent_openai.agent.agent_template import *
from app.agent_openai.tools.web_search import GoogleSearch
from app.agent_openai.tools.rag_search import RagSearch
from app.agent_openai.tools.rag_search_chroma import ChromaRagSearch
from app.agent_openai.tools.spotify_search import SpotifySearch
from app.agent_openai.tools.youtube_search import YoutubeSearch
from app.agent_openai.tools.custom_sd import sculpture
from app.agent_openai.tools.introduce import introduce, default


class CustomPromptTemplate(StringPromptTemplate):
    template: str
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        intermediate_steps = kwargs.pop("intermediate_steps")
        # 没有互联网查询信息
        related_content = "\n"
        action_content = "\n"
        if len(intermediate_steps) == 0:
            background_infomation = "\n"
            template = router_template

        # 返回了背景信息
        else:
            # 根据 intermediate_steps 中的 AgentAction 拼装 background_infomation
            background_infomation = "\n\n你还有这些已知信息作为参考：\n\n"
            action, observation = intermediate_steps[0]
            if isinstance(observation, tuple) or isinstance(observation, list):
                background_infomation += observation[0]
                related_content += observation[1]
            else:
                background_infomation += f"{observation}\n"
            if "Default" == action.tool or "History" == action.tool:
                template = generate_template_zh
            elif "Introduce" == action.tool:
                return observation
            else:
                # todo 先默认返回空，后续再看
                template = action_template_zh
                action_content = observation

        kwargs["background_content"] = background_infomation
        kwargs["related_content"] = related_content
        kwargs["action_content"] = action_content
        return template.format(**kwargs)


# 匹配每个tool的格式
class CustomOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # 正则表达式模式，用于匹配所需的格式
        pattern = r"(History|Music|Video|Painting|Introduce|Web|Default)\('([^']*)'\)"

        # 使用 re.match 检查字符串是否与模式匹配
        match = re.match(pattern, llm_output)

        # 如果llm没有返回History|Music|Video|Default则认为直接结束指令
        if not match:
            return AgentFinish(
                return_values={"output": llm_output.strip()},
                log=llm_output,
            )
        # 否则的话都认为需要调用Tool
        else:

            action = match.group(1).strip()
            action_input = match.group(2).strip()
            return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)


class DeepAgent:
    tool_names: str = ""
    agent_executor: any
    tools: List[Tool]
    llm_chain: any

    def query(self, query: str = "", chat_history: str = ""):
        # tool_name = self.tool_name
        result = self.agent_executor.run(chat_history=chat_history, input=query, tool_name="")
        return result

    def __init__(self, **kwargs):
        llm = CustomLLM()
        tools = [
            Tool.from_function(
                func=default,
                name="Default",
                description="Use this when it is impossible to categorize the question or when the larger model thinks it can be answered."
            ),
            Tool.from_function(
                func=GoogleSearch.web_search,
                name="Web",
                description="Utilize the default web search tool to investigate the user's query, focusing on the most recent web pages that provide explanations. The findings should be used as reference material for the large model."
            ),
            Tool.from_function(
                func=ChromaRagSearch.rag_search,
                name="History",
                description="This method involves researching historical information related to the user's question, providing relevant information to the AI assistant for reference during processing."
            ),
            Tool.from_function(
                func=SpotifySearch.search_download_songs,
                name="Music",
                description="Call this method when user need to play a song, the first parameter song_name is the song to be played, it can not be null; the second parameter artist is the author of the song, it can be null. Example of parameters \"song_name,artist\". The method returns the played information to the user."
            ),
            Tool.from_function(
                func=YoutubeSearch.search_and_play,
                name="Video",
                description="This method is called when the user needs to play a video, the parameter video_name indicates the name of the video to be played. Search and play the specified video content through youtube webpage, and return the played information to the user after execution."
            ),
            Tool.from_function(
                func=sculpture,
                name="Painting",
                description="This method is used for user drawing-related needs, providing the ability to generate images based on the text, the user inputs a description of the image-related instructions, the method returns the corresponding image output"
            ),
            Tool.from_function(
                func=introduce,
                name="Introduce",
                description="This method is used when the user needs the Agent to introduce itself."
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


if __name__ == "__main__":
    agent = DeepAgent()
    agent.query("续写诗词，万里千山只等君前")
