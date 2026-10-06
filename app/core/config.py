# import os 

# from dotenv import load_dotenv

# load_dotenv()

# POSTGRES_DB = os.getenv("POSTGRES_DB")
# POSTGRES_USER=os.getenv("POSTGRES_USER")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# DATABASE_URL = (
#     f"postgresql+psycopg2://"
#     f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
#     f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
# )



from  pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_DB:str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"

    GROQ_API_KEY:str
    GITHUB_TOKEN:str

    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


    @property
    def DATABASE_URL(self)-> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

settings=Settings()