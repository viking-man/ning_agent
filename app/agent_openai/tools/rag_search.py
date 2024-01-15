from app.agent_openai.rag.custom_rag import LocalDocQA
import torch.cuda
import torch.backends
from app.agent_openai.agent.agent_config import *
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.agents import tool
from app.agent_openai.tools.web_search import GoogleSearch

EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
embeddings = HuggingFaceEmbeddings(model_name="GanymedeNil/text2vec-large-chinese",
                                   model_kwargs={'device': EMBEDDING_DEVICE})

localDocQA = LocalDocQA(filepath=LOCAL_CONTENT,
                        vs_path=VS_PATH,
                        embeddings=embeddings,
                        init=True)

googleSearch = GoogleSearch()


class RagSearch:

    @tool
    def rag_search(query: str = ""):
        """This method involves researching historical and philosophical literature related to the user's question,
        providing relevant information to the AI assistant for reference during processing."""
        related_content = localDocQA.query_knowledge(query=query)
        formed_related_content = "\n" + related_content
        current_content = googleSearch.web_search(query)

        return formed_related_content, current_content
