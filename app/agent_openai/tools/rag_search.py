from rag import LocalDocQA
import torch.cuda
import torch.backends
from agent_config import *
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.agents import Tool
from tools import GoogleSearch

EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
embeddings = HuggingFaceEmbeddings(model_name="GanymedeNil/text2vec-large-chinese",
                                   model_kwargs={'device':EMBEDDING_DEVICE})

localDocQA = LocalDocQA(filepath=LOCAL_CONTENT,
                    vs_path=VS_PATH,
                    embeddings=embeddings,
                    init=True)

googleSearch =  GoogleSearch()

class RagSearch:
    
    @Tool
    def search(query:str = ""):
        related_content = localDocQA.query_knowledge(query=query)
        formed_related_content = "\n" + related_content
        current_content = googleSearch.search(query)
        
        return formed_related_content,current_content
        
        