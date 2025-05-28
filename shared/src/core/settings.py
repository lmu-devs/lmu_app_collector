from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from shared.src.settings.llm_settings import AnthropicConfig, OpenAIConfig


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "LMU App Backend"
    openai_config: OpenAIConfig = OpenAIConfig()
    anthropic_config: AnthropicConfig = AnthropicConfig()

    # Environment
    ENVIRONMENT: str

    # Deployment
    DOCKER_USERNAME: str


    # API keys for external services
    DEEPL_API_KEY: str
    TMDB_API_KEY: str
    OMDB_API_KEY: str

    # AI Keys
    OPENAI_API_KEY: str

    # CMS
    DIRECTUS_ACCESS_TOKEN: str
    DIRECTUS_BASE_URL: str = Field(
        default="https://cms.lmu-dev.org",
        description="Using internal docker container for production (http://directus:8055)",
    )
    DIRECTUS_EXTERNAL_URL: str = "https://cms.lmu-dev.org"

    class ConfigDict:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
