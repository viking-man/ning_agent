import requests
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

RapidAPIKey = "3b5dd7d5f5mshd78f146dc498a60p143d49jsn07023d199750"

class GoogleSearch:
    def search(query: str = ""):
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


class WikiSearch:
    def search(query:str = "c "):
        query = query.strip()

        if query == "":
            return ""
        
        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        result = wikipedia(query)
        
        return result
        