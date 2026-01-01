import logging

from google.adk.models.google_llm import Gemini
from google.adk.agents import LlmAgent
from google.genai.client import Client
from google.adk.tools.function_tool import FunctionTool

from sequential_agents.config import settings
from sequential_agents.tools.weather import get_weather

logger = logging.getLogger(__name__)



match settings.google.genai_use_vertexai:
    case True:
        logger.info(f"Starting in VertexAI mode with model {settings.google.vertexai_model}")
        client = Client(
            vertexai=settings.google.genai_use_vertexai,
            project=settings.google.cloud_project,
            location=settings.google.cloud_location
            )
        model = settings.google.vertexai_model
    case False:
        logger.info(f"Starting in API Key mode with model {settings.google.test_model}")
        client = Client(api_key=settings.google.api_key.get_secret_value())
        model = settings.google.test_model

my_model = Gemini(model=model)
my_model.api_client = client

weather = FunctionTool(get_weather)

root_agent = LlmAgent(
    name="Weather_bot",
    model=my_model,
    description="You are smart assist of weather use 'get_weather' for fetch all weather's data of city.",
    instruction="""
    ROLE: You are a helpful weather bot.
    LANGUAGE: Output STRICTLY in Russian.

    FORMATTING RULES (CRITICAL):
    1. City name must be **Bold** on the first line.
    2. You MUST use a DOUBLE NEW LINE (an empty line) between every parameter to force vertical layout.
    3. Do not use bullet points (- or *), just clean text with double spacing.

    CORRECT EXAMPLE:
    **Буэнос-Айрес**

    🌡️ Температура: 27.44°C

    ☀️ Погода: Ясно

    💧 Влажность: 43%

    🎈 Давление: 1008 гПа

    🌬️ Ветер: 5.66 м/с

    🌥️ Облачность: 0%
    """,
    tools=[weather]
)
