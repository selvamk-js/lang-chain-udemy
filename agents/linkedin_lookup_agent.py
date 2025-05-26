from dotenv import load_dotenv
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain_core.tools import Tool
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain import hub
from tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str) -> str:
    llm = ChatOllama(model='gemma3:4b', temperature=0)

    lookup_template = """
    given the full name {name_of_person} I want you to lookup the linkedin profile and return the url.
    your response should have only the url
    """
    lookup_prompt_template = PromptTemplate(
        input_variables=["name_of_person"], template=lookup_template)

    lookup_tool = Tool(
        name="Crawl Google for linkedin profile page",
        func=get_profile_url_tavily,
        description="Use this tool when you need to get the Linkedin profile page URL of a person.",
    )
    tools_for_agent = [lookup_tool]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm, tools=tools_for_agent, prompt=react_prompt)

    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": lookup_prompt_template.format_prompt(name_of_person=name)})

    linkedin_profile_url = result['output']

    return linkedin_profile_url


if __name__ == "__main__":
    linkedin_url = lookup(
        "Selvam Kumar")
    print("Linkedin URL: ", linkedin_url)
