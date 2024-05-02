from flask import Blueprint

# 查询/唱歌/绘画
bp = Blueprint('agent_llama', __name__)

from app.agent_llama import agent_facade
