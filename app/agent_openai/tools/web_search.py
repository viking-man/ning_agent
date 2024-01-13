from langchain.agents import tool
import requests

RapidAPIKey = "3b5dd7d5f5mshd78f146dc498a60p143d49jsn07023d199750"

#默认的web搜索工具，查询用户输入的问题最新的网页解释，给大模型作为参考资料

class GoogleSearch:
    
    @tool
    def search(question:str = ""):
        """Utilize the default web search tool to investigate the user's query, focusing on the most recent web pages that provide explanations. The findings should be used as reference material for the large model."""
        query = query.strip()

        if query == "":
            return ""

        if RapidAPIKey == "":
            return "请配置你的 RapidAPIKey"

        url = "https://google-web-search1.p.rapidapi.com/"
        
        querystring = {"query":query,"limit":"3","related_keywords":"true"}

        headers = {
            "X-RapidAPI-Key": RapidAPIKey,
            "X-RapidAPI-Host": "google-web-search1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        
        data_list = response.json()['results']

        if len(data_list) == 0:
            return ""
        else:
            result_arr = []
            result_str = ""
            for i in range(3):
                item = data_list[i]
                title = item["title"]
                description = item["description"]
                item_str = f"{title}: {description}"
                result_arr = result_arr + [item_str]

            result_str = "\n".join(result_arr)
            return result_str
    
    