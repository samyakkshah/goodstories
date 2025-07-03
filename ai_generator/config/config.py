import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings:
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: Optional[str] = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_KEY: Optional[str] = os.getenv("SUPABASE_SERVICE_KEY")
    APP_PORT: Optional[int] = int(os.getenv("APP_PORT"))


settings = Settings()
