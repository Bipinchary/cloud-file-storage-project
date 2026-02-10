from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    ENV: str = "local"

    AWS_REGION: str
    AWS_S3_BUCKET: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_ACCESS_KEY_ID: str
    class Config:
        env_file = ".env"
        extra = "forbid"


settings = Settings()
