from app.open_ai import gpt_prompt
from app.type import ChatGPTModel
from app.models import Chat, Audio
import logging

import openai
from app import db
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('../../.flaskenv', override=True)

# 获取环境变量
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)


def get_chat_history(user_id, chat_id, gpt_version):
    # 查询聊天记录
    chat_record = Chat.query.filter_by(chat_id=chat_id).filter_by(user_id=user_id).first()
    if chat_record is None:
        chat_history = []
    else:
        chat_history = json.loads(chat_record.chat_history)

    return chat_history, chat_record


def text_chat(user_message, user_id, chat_id, gpt_version):
    chat_history, chat_record = get_chat_history(user_id, chat_id, gpt_version)
    gpt_model = ChatGPTModel.get_value(gpt_version)

    # request openai
    ai_message, chat_history = requestOpenai(user_message, chat_history, gpt_model)

    chat_history_json = json.dumps(chat_history)
    # 更新数据库
    if chat_record is None:
        chat_record = Chat(user_id=user_id, chat_id=chat_id, chat_history=chat_history_json)
        db.session.add(chat_record)
        logging.info(f'Add chat record->{str(chat_record)}')
        print(str(chat_record))
    else:
        chat_record.chat_history = chat_history_json
        logging.info(f'Update chat record->{str(chat_record)}')
    db.session.commit()

    return ai_message, chat_history


def requestOpenai(chat_context, chat_history, model):
    # 第一次请求，带上英语口语老师对应的prompt

    if len(chat_history) == 0:
        chat_history.append({"role": "system",
                             "content": gpt_prompt.english_teacher_prompt})
    chat_history.append({"role": "user",
                         "content": chat_context})
    print(f'openai chat request->{chat_history}')

    # response = openai.ChatCompletion.create(
    #     model=model,
    #     messages=chat_history,
    #     temperature=0
    # )

    response = client.chat.completions.create(
        model=model,
        messages=chat_history,
        temperature=0
    )

    print(f'openai chat response->{str(response)}')
    # content_ = response.choices[0]['message']['content']
    content_ = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": content_})
    return content_, chat_history
