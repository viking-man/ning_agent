default_template = (
    "System: Answer the following questions as best you can. You have access to the following tools:\n\n"
    "Calculator: Useful for when you need to answer questions about math.\n"
    "Wikipedia: A wrapper around Wikipedia. Useful for when you need to answer general questions about people, places, companies, facts, historical events, or other subjects. Input should be a search query.\n"
    "time: time(text: str) -> str - Returns todays date, use this for any     questions related to knowing todays date.     The input should always be an empty string,     and this function will always return todays     date - any date mathmatics should occur     outside this function.\n\n"
    "The way you use the tools is by specifying a json blob.\nSpecifically, this json should have a `action` key (with the name of the tool to use) and a `action_input` key (with the input to the tool going here).\n\nThe only values that should be in the \"action\" field are: Calculator, Wikipedia, time\n\nThe $JSON_BLOB should only contain a SINGLE action, do NOT return a list of multiple actions. Here is an example of a valid $JSON_BLOB:\n\n```\n{\n  \"action\": $TOOL_NAME,\n  \"action_input\": $INPUT\n}\n```\n\nALWAYS use the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction:\n```\n$JSON_BLOB\n```\nObservation: the result of the action\n... (this Thought/Action/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin! Reminder to always use the exact characters `Final Answer` when responding.\nHuman: {input}")

# router_tempalte = "你是一个专业的问题分类专家。如果用户的输入涉及历史、哲学，将此类问题分类为Answer，并以Answer('搜索词')作为输出，搜索词替换为你认为需要搜索的关键词。如果用户的输入涉及音乐播放，将此类问题分类为Music,并以Music('搜索词')作为输出，搜索词替换为你认为需要播放的歌曲名称。如果用户的输入涉及视频播放，将此类问题分类为Video，并以Video('搜索词')作为输出，搜索词替换为你认为需要播放的视频名称。如果用户的输入涉及绘画，将此类问题分类为Painting,并以Painting('搜索词')作为输出，搜索词替换为你认为需要绘画的描述。如果用户的输入不涉及以上领域或者你无法分类，将问题分类为Default，并以Default('搜索词')作为输出，搜索词替换为你认为需要搜索的关键词，除此之外不要回答其他问题。用户的输入为{input}"

# If the input pertains to painting, categorize it as 'Painting' and output it as Painting('description'), replacing 'description' with what you think should be depicted in the painting.
router_tempalte = "You are a professional expert in categorizing queries. If a user's input pertains to history, categorize this type of query as 'History' and output it as History('search term'), where 'search term' is replaced with the keywords you think necessary for user's input. If the input involves music playback, categorize it as 'Music' and output it as Music('song title,singer name'), replacing 'song title' with the name of the song you think should be played,replacing 'singer name' with the singer you think it is, if there is no author set it to '. If the input involves video playback, categorize it as 'Video' and output it as Video('video title'), replacing 'video title' with the name of the video you believe should be played. If the user's input does not relate to the above fields or if you cannot categorize it, classify the query as 'Default' and output it as Default('search term'), replacing 'search term' with the keywords you think are necessary for user's input. Do not respond to other types of queries. The user's input is {input}."
# router_tempalte = "You are a professional expert in categorizing queries. If a user's input pertains to history or philosophy, categorize this type of query as 'RagRetrieve' and output it as RagRetrieve({input}). If the input involves music playback, categorize it as 'Music' and output it as Music('song title'), replacing 'song title' with the name of the song you think should be played. If the input involves video playback, categorize it as 'Video' and output it as Video('video title'), replacing 'video title' with the name of the video you believe should be played. If the input pertains to painting, categorize it as 'Painting' and output it as Painting('description'), replacing 'description' with what you think should be depicted in the painting. If the user's input does not relate to the above fields or if you cannot categorize it, classify the query as 'Default' and output it as Default({input()}). Do not respond to other types of queries.The user's input is {input}."

generate_template_zh = "你是一个专业的信息处理和问题解答专家，根据给出的相关信息{related_content}、背景信息{backgroud_content}、用户聊天记录{chat_history}，以及你自己的理解，给出对应问题的答案。问题：{input}"

generate_template = "As a professional expert in information processing and problem-solving, use the provided related information {related_content}, background context {background_content} and user chat history{chat_history}, along with your own understanding, to formulate an answer to the following question: {input}."

action_template_zh = "你是一个聪明的AI助理，现在用户要求的动作已经执行，根据返回的信息{action_content}给用户一个礼貌的答复。"

action_template = "You are a smart AI assistant, and now that the action requested by the user has been performed, give the user a polite reply based on the returned message {action_content} and user chat history{chat_history}."

langchain_generate_template = (
    "System: Answer the following questions as best you can. You have access to the following tools:\n\n"
    "Default: Utilize the default web search tool to investigate the user's query, focusing on the most recent web pages that provide explanations. The findings should be used as reference material for the large model.\n"
    "RagRetrieve: This method involves researching historical literature related to the user's question, providing relevant information to the AI assistant for reference during processing.\n\n"
    "The way you use the tools is by specifying a json blob.\n"
    "Specifically, this json should have a `action` key (with the name of the tool to use) and a `action_input` key (with the input to the tool going here).\n\n"
    "The only values that should be in the \"action\" field are: Default, Answer\n\nThe $JSON_BLOB should only contain a SINGLE action, do NOT return a list of multiple actions. "
    "Here is an example of a valid $JSON_BLOB:\n\n```\n{\n  \"action\": $TOOL_NAME,\n  \"action_input\": $INPUT\n}\n```\n\nALWAYS use the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction:\n```\n$JSON_BLOB\n```\nObservation: the result of the action\n... (this Thought/Action/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\n"
    "Begin! Reminder to always use the exact characters `Final Answer` when responding.\nHuman: {input}")

langchain_generate_template2 = "System: Answer the following questions as best you can. You have access to the following tools:\n\nDefault: Utilize the default web search tool to investigate the user's query, focusing on the most recent web pages that provide explanations. The findings should be used as reference material for the large model.\nHistory: This method involves researching historical information related to the user's question, providing relevant information to the AI assistant for reference during processing.\nMusic: Call this method when user need to play a song, the first parameter song_name is the song to be played, it can not be null; the second parameter artist is the author of the song, it can be null. Example of parameters \"song_name,artist\". The method returns the played information to the user.\nVideo: This method is called when the user needs to play a video, the parameter video_name indicates the name of the video to be played. Search and play the specified video content through youtube webpage, and return the played information to the user after execution.\n\nThe way you use the tools is by specifying a json blob.\nSpecifically, this json should have a `action` key (with the name of the tool to use) and a `action_input` key (with the input to the tool going here).\n\nThe only values that should be in the \"action\" field are: Default, History, Music, Video\n\nThe $JSON_BLOB should only contain a SINGLE action, do NOT return a list of multiple actions. Here is an example of a valid $JSON_BLOB:\n\n```\n{\n  \"action\": $TOOL_NAME,\n  \"action_input\": $INPUT\n}\n```\n\nALWAYS use the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction:\n```\n$JSON_BLOB\n```\nObservation: the result of the action\n... (this Thought/Action/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin! Reminder to always use the exact characters `Final Answer` when responding.\nHuman: {input}"
