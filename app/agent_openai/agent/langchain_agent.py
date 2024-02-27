from langchain.agents import load_tools, initialize_agent, Tool, AgentExecutor, AgentType
from langchain.chat_models import ChatOpenAI
from app.type import ChatGPTModel
from app.open_ai.openai_config import OPENAI_API_KEY
from app.agent_openai.tools.web_search import GoogleSearch
from app.agent_openai.tools.rag_search import RagSearch
from app.agent_openai.tools.spotify_search import SpotifySearch
from app.agent_openai.tools.youtube_search import YoutubeSearch
from app.agent_openai.tools.bilibili_search import BilibiliSearch
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
        ]

        self.agent_executor = initialize_agent(
            tools,
            llm,
            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            verbose=True)

    def agent_execute(self, input: str = ""):
        logging.info(f"执行Agent查询,输入{input}")
        result = self.agent_executor.run(input=input)
        logging.info(f"执行Agent查询,输入{input}，输出{result}")
        return result


if __name__ == "__main__":
    print(OPENAI_API_KEY)
    import langchain

    langchain.debug = True
    print(OPENAI_API_KEY)
    agent = LangchainAgent()
    result = agent.agent_execute("我想听汪峰的当我想你的时候")
    print(result)
