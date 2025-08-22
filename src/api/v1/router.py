from fastapi import APIRouter, Depends

from src.api.deps import get_auth
from src.api.v1 import building, activity  # , organization

api_router = APIRouter(dependencies=[Depends(get_auth)])

api_router.include_router(building.router, prefix="/buildings", tags=["buildings"])
api_router.include_router(activity.router, prefix="/activities", tags=["activities"])
# api_router.include_router(
#     organization.router, prefix="/organizations", tags=["organizations"]
# )
