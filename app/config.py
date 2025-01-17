from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    openai_api_key: str = ""
    gpt_model: str = "gpt-4o-mini"
    fireflies_api_key: str = ""
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)


config = Config()
