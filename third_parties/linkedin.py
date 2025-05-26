import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = True):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    if mock:
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.getenv("SCRAPIN_API_KEY"),
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(api_endpoint, params=params, timeout=10)

    data = response.json().get("person")
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None, []) and k not in ["certifications"]
    }
    return data


if __name__ == "__main__":
    profile = scrape_linkedin_profile(
        "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/32f3c85b9513994c572613f2c8b376b633bfc43f/eden-marco-scrapin.json", mock=True)
    print(profile)
