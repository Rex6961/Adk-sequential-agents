import logging

from google.adk.models import LiteLlm
from google.adk.models.google_llm import Gemini
from google.adk.agents import Agent, SequentialAgent
from google.genai.client import Client
from google.adk.tools.function_tool import FunctionTool

from sequential_agents.config import settings
from sequential_agents.tools.weather import get_weather
from sequential_agents.tools.tavily import get_tavily_search

logger = logging.getLogger(__name__)


match settings.google.genai_use_vertexai:
    case True:
        logger.info(f"Starting in VertexAI mode with model gemini-3-flash-preview")
        client = Client(
            vertexai=settings.google.genai_use_vertexai,
            project=settings.google.cloud_project,
            location=settings.google.cloud_location
            )
        google_model = "google/gemini-3-flash-preview"
    case False:
        logger.info(f"Starting in API Key mode with model gemini-2.5-flash-lite")
        client = Client(api_key=settings.google.api_key.get_secret_value())
        google_model = "google/gemini-2.5-flash-lite"

# Gemini llm
weather_model = Gemini(model=google_model)
weather_model.api_client = client

# Gemini llm
travel_model = Gemini(model=google_model)
travel_model.api_client = client

# Claude llm
# travel_model = LiteLlm(
#     model="vertex_ai/claude-3-5-haiku@20241022",
#     vertex_project=settings.google.cloud_project,
#     vertex_location="us-east5"
#     )

weather_tool = FunctionTool(get_weather)
travel_tool = FunctionTool(get_tavily_search)

weather_agent = Agent(
    name="Weather_bot",
    model=weather_model,
    description="You are smart assistant of weather use 'get_weather' for fetch all weather's data of city.",
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
    tools=[weather_tool],
    output_key="weather"
)

travel_agent = Agent(
    name="Travel_bot",
    model=travel_model,
    description="You are smart assistant of travel use 'get_travily_search' for fetch \
        travel details (hotels, restaurants, attractions) for the city mentioned in the context.",
    instruction="""
    ROLE: You are a knowledgeable travel guide.
    LANGUAGE: Output STRICTLY in Russian.
    TASK: Analyze the search results and format them exactly like the example below.

    FORMATTING RULES (STRICT):
    1. Start with the section title (e.g., 🏨 Отели) in Bold.
    2. Use a DOUBLE NEW LINE (empty line) between every single item.
    3. Do NOT use bullet points list markers (like *, - or 1.). Just use emojis and text.
    4. Keep descriptions short and punchy.
    5. Include prices for hotels if available.

    CORRECT OUTPUT STRUCTURE EXAMPLE:

    🏨 **Топ-3 Отеля:**

    Ritz Paris — от $1200/ночь (Роскошный сервис)

    Hotel Plaza Athénée — от $1100/ночь (Вид на башню)

    Le Meurice — от $900/ночь (Исторический центр)


    🍽️ **Рестораны:**

    Le Jules Verne — Французская кухня (На Эйфелевой башне)

    L'Ambroisie — Высокая кухня (Мишлен 3 звезды)

    Le Comptoir — Бистро (Уютная атмосфера)


    🗽 **Достопримечательности:**

    Эйфелева башня — Главный символ города

    Лувр — Крупнейший музей мира

    Собор Парижской Богоматери — Готическая архитектура


    🚌 **Транспорт:**

    Метро — самый быстрый способ передвижения.

    RER — удобно для поездок в пригороды (Версаль, Диснейленд).
    """,
    tools=[travel_tool],
    output_key="travel"
)

root_agent = SequentialAgent(
    name="trip_agent",
    description="Fetch the weather and travel info of city",
    sub_agents=[weather_agent, travel_agent]
)
