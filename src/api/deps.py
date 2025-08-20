from fastapi import Depends

from src.core.security import api_key_auth


def get_auth(_: bool = Depends(api_key_auth)) -> bool:
    return True
