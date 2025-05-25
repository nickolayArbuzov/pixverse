from pydantic_settings import BaseSettings


class PostgresqlSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    POSTGRES_HOST: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        extra = "ignore"


postgresql_settings = PostgresqlSettings()


class RabbitMQSettings(BaseSettings):
    RABBITMQ_URL: str

    class Config:
        extra = "ignore"


rabbitmq_settings = RabbitMQSettings()


class PixVerseCredentials(BaseSettings):
    PIXVERSE_USERNAME: str
    PIXVERSE_PASSWORD: str

    class Config:
        extra = "ignore"


pixverse_credentials = PixVerseCredentials()
