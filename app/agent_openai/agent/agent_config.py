import os

MODEL_NAME = 'chatglm'
REMOTE_MODEL_PATH = ''
LOCAL_MODEL_PATH=os.path.join("G:\data\\transformers\source\chatglm\model")
LOCAL_CONTENT = os.path.join(os.path.dirname(__file__), "../../resources/docs")
# PHILOSOPHY_LOCAL_CONTENT = os.path.join(os.path.dirname(__file__), "../resources/docs/philosophy")
VS_PATH = os.path.join(os.path.dirname(__file__), "vector_store\FAISS")
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 64
VECTOR_SEARCH_TOP_K = 2
os.environ["SERPAPI_API_KEY"] = "Your SerpAPI Key"

PROMPT_TEMPLATE = """已知信息：
{context}

根据上述已知信息，简洁和专业的来回答用户的问题。如果无法从中得到答案，请给出你认为最合理的回答。答案请使用中文。 问题是：{question}"""
