from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    aws_access_key_id: str
    aws_secret_access_key: str
    aws_default_region: str = "eu-west-1"
    dynamodb_table_users: str = "nutricarta-users"

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    ses_sender_email: str
    base_url: str = "http://localhost:8000"


settings = Settings()
