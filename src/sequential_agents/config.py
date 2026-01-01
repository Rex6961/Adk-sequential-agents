from pydantic import BaseModel, SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class GoogleModel(BaseModel):
    genai_use_vertexai: bool
    cloud_location: str
    cloud_project: str

    api_key: SecretStr


class WeatherModel(BaseModel):
    api_key: SecretStr


class TavilyModel(BaseModel):
    api_key: SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__"
    )

    google: GoogleModel
    weather: WeatherModel
    tavily: TavilyModel


settings = Settings()
