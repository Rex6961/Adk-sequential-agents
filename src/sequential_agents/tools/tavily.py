from typing import Dict, Any

from tavily import TavilyClient

from sequential_agents.config import settings

tavily_client = TavilyClient(api_key=settings.tavily.api_key.get_secret_value())


def get_tavily_search(city: str) -> Dict[str, Any]:
    """
    Search for travel info (hotels, restaurants, attractions) for a given city.

    :param city: The city name.
    :type city: str
    :return: Fetch travel info (hotels, restaurants, attractions)
    :rtype: Dict[str, Any]
    """
    search_result = tavily_client.search(
        query=f"""
        Travel guide for {city}:
        top 3 hotels with prices per night,
        top 3 restaurants with cuisine type,
        main tourist attractions,
        public transportation tips.
        """,
        search_depth="advanced",
        max_results=7,
        include_answer="advanced"
    )
    return search_result
