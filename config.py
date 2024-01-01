from pydantic_settings import BaseSettings
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str
    DATABASE_URL: str
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str
    SECRET_KEY: str
    CLIENT_ORIGIN: str

    class Config:
        env_file = './.env'


settings = Settings()
client = AsyncIOMotorClient(settings.DATABASE_URL)
db = client.get_database("rchat")
engine = AIOEngine(client=client, database="rchat")
