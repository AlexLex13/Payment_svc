from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    redis_host: str
    redis_port: str

    class Config:
        env_file = ".env"


settings = Settings()
