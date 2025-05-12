#用于加载.env
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL:str
    APP_ENV:str="debelopment"

class Config:
    env_file=".env"

settings = Settings()

