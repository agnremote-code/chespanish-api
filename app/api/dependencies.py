from app.core.config import get_settings
from app.services.supabase_auth import SupabaseAuthService


def get_auth_service() -> SupabaseAuthService:
    return SupabaseAuthService(get_settings())
