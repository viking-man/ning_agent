from ..agent.agent_core import NingAgent


ning_agent = NingAgent()

def dispatch(chat: str = "", chat_history: str = ""):
    content = ning_agent.query(chat, chat_history)
    return content


if __name__ == "__main__":
    
    dispatch("文明的起源")