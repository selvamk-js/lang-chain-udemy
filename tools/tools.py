from langchain_tavily import TavilySearch
import os


def get_profile_url_tavily(name: str) -> str:
    """search for the linkedin profile url of a person using tavily"""
    search = TavilySearch(api_key=os.getenv("TAVILY_API_KEY"))
    # result = search.invoke({"query": f"{name} linkedin profile"})
    # print(result)
    res = search.run(
        f"{name} LinkedIn Conexus Software Solutions Associate Manager")
    print(res)
    return res
