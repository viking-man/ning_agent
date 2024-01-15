from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv('../../.flaskenv', override=True)
# 获取环境变量
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')