"""
This module provides functionality for an ice breaker application using LangChain.
It handles environment variables and API key configuration.
"""
# import os
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
# from langchain.schema import StrOutputParser
from agents.linkedin_lookup_agent import lookup
from third_parties.linkedin import scrape_linkedin_profile
from output_parser import summary_parser


# Load environment variables from .env file
load_dotenv()

INFORMATION = """
Elon Reeve Musk (/ˈiːlɒn/ EE-lon; born June 28, 1971) is a businessman known for his leadership of Tesla, SpaceX, and X (formerly Twitter). Since 2025, he has been a senior advisor to United States president Donald Trump and the de facto head of the Department of Government Efficiency (DOGE). Musk has been considered the wealthiest person in the world since 2021; as of May 2025, Forbes estimates his net worth to be US$424.7 billion. He was named Time magazine's Person of the Year in 2021.

Born to a wealthy family in Pretoria, South Africa, Musk emigrated in 1989 to Canada. He graduated from the University of Pennsylvania in the U.S. before moving to California to pursue business ventures. In 1995, Musk co-founded the software company Zip2. Following its sale in 1999, he co-founded X.com, an online payment company that later merged to form PayPal, which was acquired by eBay in 2002. That year, Musk also became a U.S. citizen.

In 2002, Musk founded the space technology company SpaceX, becoming its CEO and chief engineer; the company has since led innovations in reusable rockets and commercial spaceflight. Musk joined the automaker Tesla as an early investor in 2004 and became its CEO and product architect in 2008; it has since become a leader in electric vehicles. In 2015, he co-founded OpenAI to advance artificial intelligence research but later left; growing discontent with the organization's direction in the 2020s led him to establish xAI. In 2022, he acquired the social network Twitter, implementing significant changes and rebranding it as X in 2023. In January 2025, he was appointed head of Trump's newly created DOGE. His other businesses include the neurotechnology company Neuralink, which he co-founded in 2016, and the tunneling company the Boring Company, which he founded in 2017.

Musk's political activities and views have made him a polarizing figure. He has been criticized for making unscientific and misleading statements, including COVID-19 misinformation and promoting conspiracy theories, and affirming antisemitic, racist, and transphobic comments. His acquisition of Twitter was controversial due to a subsequent increase in hate speech and the spread of misinformation on the service. Especially since the 2024 U.S. presidential election, Musk has been heavily involved in politics as a vocal supporter of Trump. Musk was the largest donor in the 2024 U.S. presidential election and is a supporter of global far-right figures, causes, and political parties. His role in the second Trump administration, particularly in regards to DOGE, has attracted public backlash.
# """


def ice_break_with_linkedin(name: str) -> str:
    # linkedin_url = lookup(name)
    linkedin_url = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/32f3c85b9513994c572613f2c8b376b633bfc43f/eden-marco-scrapin.json"
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_url, mock=True)
    SUMMARY_TEMPLATE = """
    given the Linkedin information {information} about a person from I want you to create:
    - a short summary
    - two interesting facts about them
    - what to call them
    - a short fun fact about them
    \n{format_instructions}
    """
    summary_propmpt_template = PromptTemplate(
        input_variables=["information"], template=SUMMARY_TEMPLATE,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()})

    llm = ChatOllama(model="gemma3:4b", temperature=0)

    chain = summary_propmpt_template | llm | summary_parser

    res = chain.invoke({"information": linkedin_data})
    return res


if __name__ == "__main__":
    print("Hello LangChain")
    res = ice_break_with_linkedin("Nandhini Anandhan")
    print(res)
