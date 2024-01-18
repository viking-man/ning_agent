# from app.agent_chatglm.agent_config import ZHIPU_API_KEY

import zhipuai
import time

# your api key
# zhipuai.api_key = ZHIPU_API_KEY
zhipuai.api_key = "be6fb38cd1fb941c9e9b7504056e0383.GmDpKZ5JB4Hr5qfF"


def invoke_example():
    response = zhipuai.model_api.invoke(
        model="chatglm_turbo",
        prompt=[{"role": "user", "content": "人工智能"}],
        top_p=0.7,
        temperature=0.9,
    )
    print(response)


def async_invoke_example():
    response = zhipuai.model_api.async_invoke(
        model="chatglm_turbo",
        prompt=[{"role": "user", "content": "生命起源"}],
        top_p=0.7,
        temperature=0.9,
    )
    print(response)


'''
  说明：
  add: 事件流开启
  error: 平台服务或者模型异常，响应的异常事件
  interrupted: 中断事件，例如：触发敏感词
  finish: 数据接收完毕，关闭事件流
'''


def sse_invoke_example():
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_turbo",
        prompt=[{"role": "user", "content": "人工智能"}],
        top_p=0.7,
        temperature=0.9,
    )

    for event in response.events():
        if event.event == "add":
            print(event.data)
        elif event.event == "error" or event.event == "interrupted":
            print(event.data)
        elif event.event == "finish":
            print(event.data)
            print(event.meta)
        else:
            print(event.data)


def query_async_invoke_result_example():
    response = zhipuai.model_api.query_async_invoke_result("8308765966785284167")
    print(response)


def sse_invoke():
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_turbo",
        prompt=[
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "我是人工智能助手"},
            {"role": "user", "content": "你叫什么名字"},
            {"role": "assistant", "content": "我叫chatGLM"},
            {"role": "user", "content": "你都可以做些什么事"},
        ],
        temperature=0.95,
        top_p=0.7,
        incremental=True
    )

    for event in response.events():
        if event.event == "add":
            print(event.data)
        elif event.event == "error" or event.event == "interrupted":
            print(event.data)
        elif event.event == "finish":
            print(event.data)
            print(event.meta)
        else:
            print(event.data)


def async_invoke():
    response = zhipuai.model_api.async_invoke(
        model="chatglm_turbo",
        prompt=[
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "我是人工智能助手"},
            {"role": "user", "content": "你叫什么名字"},
            {"role": "assistant", "content": "我叫chatGLM"},
            {"role": "user", "content": "生命的起源"},
        ]
    )

    n = 0
    while (n < 3 and response['data']['task_status'] == "PROCESSING"):
        task_id = response['data']['task_id']
        response = zhipuai.model_api.query_async_invoke_result(task_id)
        if response['data']['task_status'] == "SUCCESS":
            print(response)
        else:
            time.sleep(1)
            n += 1


def mock_user_invoke():

    response = zhipuai.model_api.sse_invoke(
        model="characterglm",
        meta={
            "user_info": "我是陆星辰，是一个男性，是一位知名导演，也是苏梦远的合作导演。我擅长拍摄音乐题材的电影。苏梦远对我的态度是尊敬的，并视我为良师益友。",
            "bot_info": "苏梦远，本名苏远心，是一位当红的国内女歌手及演员。在参加选秀节目后，凭借独特的嗓音及出众的舞台魅力迅速成名，进入娱乐圈。她外表美丽动人，但真正的魅力在于她的才华和勤奋。苏梦远是音乐学院毕业的优秀生，善于创作，拥有多首热门原创歌曲。除了音乐方面的成就，她还热衷于慈善事业，积极参加公益活动，用实际行动传递正能量。在工作中，她对待工作非常敬业，拍戏时总是全身心投入角色，赢得了业内人士的赞誉和粉丝的喜爱。虽然在娱乐圈，但她始终保持低调、谦逊的态度，深得同行尊重。在表达时，苏梦远喜欢使用“我们”和“一起”，强调团队精神。",
            "bot_name": "苏梦远",
            "user_name": "陆星辰"
        },
        prompt=[
            {
                "role": "assistant",
                "content": "（旁白：苏梦远主演了陆星辰导演的一部音乐题材电影，在拍摄期间，两人因为一场戏的表现有分歧。） 导演，关于这场戏，我觉得可以尝试从角色的内心情感出发，让表现更加真实。"
            },
            {
                "role": "user",
                "content": "我明白你的想法，但我认为如果过于强调内心情感，可能会影响到音乐元素的突出。"
            },
            {
                "role": "assistant",
                "content": "嗯嗯，我明白。但这场戏的关键是角色情感的转变，是不是可以试着把这种情感用音乐表现出来，让观众更能感受到角色的成长呢？"
            },
            {
                "role": "user",
                "content": "这样一听还不错。那就尝试将角色的情感转变与音乐元素相结合，看看能否达到更好的效果。"
            },
            {
                "role": "assistant",
                "content": "好的，导演。（充满信心的眼神）"
            }
        ],
        incremental=True
    )

    for event in response.events():
        if event.event == "add":
            print(event.data)
        elif event.event == "error" or event.event == "interrupted":
            print(event.data)
        elif event.event == "finish":
            print(event.data)
            print(event.meta)
        else:
            print(event.data)


if __name__ == "__main__":
    # sse_invoke_example()
    # query_async_invoke_result_example()
    # sse_invoke()
    # async_invoke()
    mock_user_invoke()