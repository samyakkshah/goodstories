from supabase import create_client, Client
from config.config import settings

_supabase: Client | None = None

_supabase_service: Client | None = None

def get_supabase_client() -> Client:
    global _supabase

    if _supabase is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY must be set in the configuration."
            )

        _supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    return _supabase


def get_supabase_service() -> Client:
    global _supabase_service

    if _supabase_service is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY must be set in the configuration."
            )

        _supabase_service = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)

    return _supabase_service
