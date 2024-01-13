import torch.cuda
import torch.backends
from typing import Any, List, Dict, Union, Mapping, Optional
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from ..agent.agent_llm import CustomLLM
from ..agent.agent_core import DeepAgent
from ..agent.agent_db import LocalDocQA
from ..agent.agent_config import *
EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

deep_agent = DeepAgent()

embeddings = HuggingFaceEmbeddings(model_name="GanymedeNil/text2vec-large-chinese",
                                   model_kwargs={'device':EMBEDDING_DEVICE})

qa_doc = LocalDocQA(filepath=LOCAL_CONTENT,
                    vs_path=VS_PATH,
                    embeddings=embeddings,
                    init=True)

def answer(query: str = ""):
    question = query
    related_content = qa_doc.query_knowledge(query=question)
    formed_related_content = "\n" + related_content
    result = deep_agent.query(related_content=formed_related_content, query=question)
    return result

if __name__ == "__main__":
    question = "人类起源是什么"
    related_content = qa_doc.query_knowledge(query=question)
    formed_related_content = "\n" + related_content
    print(deep_agent.query(related_content=formed_related_content, query=question))
