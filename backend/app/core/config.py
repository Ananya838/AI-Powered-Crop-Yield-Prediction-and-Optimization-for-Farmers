from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Crop Yield AI Platform"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "change-this-secret"
    access_token_expire_minutes: int = 60 * 24 * 7

    database_url: str | None = None

    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = "root"
    mysql_db: str = "crop_ai"

    redis_url: str = "redis://localhost:6379/0"
    ml_model_path: str = "models/best_yield_model.joblib"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    @property
    def sqlalchemy_database_uri(self) -> str:
        if self.database_url:
            return self.database_url

        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@"
            f"{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"
        )


settings = Settings()
