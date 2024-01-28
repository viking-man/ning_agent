# from app.agent_chatglm.agent_config import ZHIPU_API_KEY
import logging

import zhipuai
import time
from zhipuai import ZhipuAI
import base64
from PIL import Image
import io

# your api key
# zhipuai.api_key = ZHIPU_API_KEY
zhipuai.api_key = "be6fb38cd1fb941c9e9b7504056e0383.GmDpKZ5JB4Hr5qfF"
client = ZhipuAI(api_key="be6fb38cd1fb941c9e9b7504056e0383.GmDpKZ5JB4Hr5qfF")  # 请填写您自己的APIKey


def invoke():
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "system", "content": "你是一个聪明且富有创造力的小说作家"},
            {"role": "user",
             "content": "请你作为童话故事大王，写一篇短篇童话故事，故事的主题是要永远保持一颗善良的心，要能够激发儿童的学习兴趣和想象力，同时也能够帮助儿童更好地理解和接受故事中所蕴含的道理和价值观。"}
        ],
        stream=True,
    )
    for chunk in response:
        print(chunk.choices[0].delta)


def async_invoke():
    response = client.chat.asyncCompletions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content": "请你作为童话故事大王，写一篇短篇童话故事，故事的主题是要永远保持一颗善良的心，要能够激发儿童的学习兴趣和想象力，同时也能够帮助儿童更好地理解和接受故事中所蕴含的道理和价值观。"
            }
        ],
    )
    print(response)


def sse_invoke():
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "system", "content": "你是一个人工智能助手，你叫叫chatGLM"},
            {"role": "user", "content": "你好！你叫什么名字"},
        ],
        stream=True,
    )
    for chunk in response:
        print(chunk.choices[0].delta)


def system_prompt():
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "system", "content": "你是一个聪明且富有创造力的小说作家"},
            {"role": "user",
             "content": "请你作为童话故事大王，写一篇短篇童话故事，故事的主题是要永远保持一颗善良的心，要能够激发儿童的学习兴趣和想象力，同时也能够帮助儿童更好地理解和接受故事中所蕴含的道理和价值观。"}
        ],
        stream=True,
    )
    for chunk in response:
        print(chunk.choices[0].delta)


def function_invoke():
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content": "你能帮我查询2024年1月1日从北京南站到上海的火车票吗？"
            }
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "query_train_info",
                    "description": "根据用户提供的信息，查询对应的车次",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "departure": {
                                "type": "string",
                                "description": "出发城市或车站",
                            },
                            "destination": {
                                "type": "string",
                                "description": "目的地城市或车站",
                            },
                            "date": {
                                "type": "string",
                                "description": "要查询的车次日期",
                            },
                        },
                        "required": ["departure", "destination", "date"],
                    },
                }
            }
        ],
        tool_choice="auto",
    )
    print(response.choices[0].message)


def vision_invoke():
    encoded_string = image_to_base64("/Users/viking/ai/develope/ning_agent/app/static/robot.png")
    response = client.chat.completions.create(
        model="glm-4v",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "图里有什么"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": encoded_string
                        }
                    }
                ]
            }
        ]
    )
    print(response.choices[0].message)


def image_to_base64(image_path):
    with Image.open(image_path) as image:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")  # Or format of your image like "PNG"
        img_str = base64.b64encode(buffered.getvalue())
        return img_str


def text_to_image():
    response = client.images.generations(
        model="cogview-3",  # 填写需要调用的模型名称
        prompt="一个鼠头鸭身的动物",
    )
    print(response.data[0].url)

if __name__ == "__main__":
    text_to_image()
