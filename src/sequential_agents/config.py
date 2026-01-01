from pydantic import BaseModel, SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class GoogleModel(BaseModel):
    genai_use_vertexai: bool
    cloud_location: str
    cloud_project: str
    vertexai_model: str = Field(default="gemini-3-pro-preview")
    
    api_key: SecretStr
    test_model: str = Field(default="gemini-2.5-flash-lite")


class WeatherModel(BaseModel):
    api_key: SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__"
    )

    google: GoogleModel
    weather: WeatherModel


settings = Settings()
