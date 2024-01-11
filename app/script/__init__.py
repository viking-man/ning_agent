from flask import Blueprint

bp = Blueprint('script', __name__)

from app.agent import agent_llm, agent_facade, langchain
