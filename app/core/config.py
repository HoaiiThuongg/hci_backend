from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Signora API"
    API_V1_PREFIX: str = "/api/v1"

    # Mặc định SQLite (aiosqlite) để chạy được mọi hệ điều hành mà không cần .env.
    # Windows/MSSQL: tạo .env với DATABASE_URL, ví dụ:
    #   DATABASE_URL=mssql+aioodbc://@localhost/SignoraDB?driver=ODBC+Driver+17+for+SQL+Server&trustservercertificate=yes
    DATABASE_URL: str = "sqlite+aiosqlite:///./dev.db"

    # CORS: danh sách origin FE được phép gọi, phân cách bằng dấu phẩy
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
