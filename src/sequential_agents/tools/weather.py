"""Weather API client module."""
import requests

from typing import Dict, Any

from pydantic import BaseModel, Field

from sequential_agents.config import settings


class WeatherType(BaseModel):
    city: str = Field(..., description="The city name.")
    temperature: float = Field(..., description="The current temperature in the city.")
    humidity: float = Field(..., description="The current humidity in the city.")
    pressure: int = Field(..., description="The current pressure in the city.")
    wind_speed: float = Field(..., description="The current wind's speed in the city.")
    clouds: int = Field(..., description="The current clouds in the city.")
    weather_main: str = Field(..., description="The current weather in the city.")


def get_weather(city: str) -> Dict[str, Any]:
    """The current weather in the city.

    Args:
        city (str): The city name.

    Returns:
        WeatherType: Return the current_city,
            temperature, humidity, pressure,
            wind_speed, rain, clouds, weather_main.
    """
    payload = {
        "q": f"{city}",
        "appid": f"{settings.weather.api_key.get_secret_value()}"
    }
    url = "https://api.openweathermap.org/data/2.5/weather?exclude=current&units=metric"

    try:
        response = requests.get(url=url, params=payload)
        response.raise_for_status()
        weather_data = response.json()

        if weather_data["cod"] == 200:
            temperature = weather_data["main"]["temp"]
            humidity = weather_data["main"]["humidity"]
            current_city = weather_data["name"]
            pressure = weather_data["main"]["pressure"]
            wind_speed = weather_data["wind"]["speed"]
            clouds = weather_data["clouds"]["all"]
            weather_main = weather_data["weather"][0]["main"]

            weather_obj = WeatherType(
                city=current_city,
                temperature=temperature,
                humidity=humidity,
                pressure=pressure,
                wind_speed=wind_speed,
                clouds=clouds,
                weather_main=weather_main,
            )

            return weather_obj.model_dump()

        else:
            return {"Error": weather_data["cod"]}
    except requests.exceptions.RequestException as e:
        return {"RequestException": f"An error occurred during the API request: {e}"}
    except KeyError as e:
        return {"KeyError": f"Error parsing data: missing key {e}"}
