import pytest
import re
import torch

def parse_input(input_string):
    # 正则表达式模式，用于匹配所需的格式
    pattern = r"(Answer|Music|Video|Painting|Default)\('([^']*)'\)"
    
    # 使用 re.match 检查字符串是否与模式匹配
    match = re.match(pattern, input_string)

    if match:
        # 提取动作名称和搜索内容
        action_name = match.group(1)
        search_content = match.group(2)
        return action_name, search_content
    else:
        # 如果字符串不符合模式，则返回 None
        return None

def test_mps():
    print(torch.backends.mps.is_available())

if __name__ == "__main__":
    # 示例使用
    test_string = "Music('Yesterday')"
    result = parse_input(test_string)
    # 这将打印结果
    print(result)




