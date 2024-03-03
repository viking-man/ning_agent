from app.agent_openai.agent.agent_template import introduce_template


def introduce(input: str):
    '''这个方法在用户需要Agent自我介绍时使用'''
    return introduce_template


def default(input: str):
    '''这个方法默认返回输入信息'''
    return input
