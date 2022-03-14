from hashlib import algorithms_available
from pydantic import BaseSettings

class Settings(BaseSettings):
  database_hostname: str = "localhost"
  database_port: int = 5432
  database_name: str = "fast_API"
  database_username: str = "postgres"
  database_password: str = "postgres"
  secret_key: str = "secret"
  algorithm: str
  access_token_expire_minutes: int

  class Config:
    env_file = ".env"
  
settings = Settings()
