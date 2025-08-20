from fastapi import Header, HTTPException, status
from src.core.config import settings


async def api_key_auth(x_api_key: str | None = Header(default=None)):
    if not x_api_key or x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return True
