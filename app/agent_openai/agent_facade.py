from agent import agent_core

def dispatch(chat:str="",chat_history:str=""):
   content =  agent_core.query(chat,chat_history)
   return content

if __name__ == "__main__":
    
    dispatch("文明的起源")