from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.models import Activity
from src.schemas.activity import ActivityCreate, ActivityOut
from src.services.activity import get_activity_service

router = APIRouter()


@router.post("/create", response_model=ActivityOut)
async def create_activity(
        activity_data: ActivityCreate, db: AsyncSession = Depends(get_db)
) -> Activity:
    """
    Создание новой деятельности
    """
    service = get_activity_service(db)
    activity = await service.create_activity(name=activity_data.name,
                                             parent_id=activity_data.parent_id)
    return activity


@router.get("/get_by_name_and_parent_name", response_model=ActivityOut)
async def get_activity_by_name_and_parent_name(
        name: str,
        parent_name: str = "",
        db: AsyncSession = Depends(get_db),
) -> Activity:
    """
    Получение деятельности по названию и имени родителя
    """
    service = get_activity_service(db)
    activity = await service.get_activity_by_name_and_parent_name(name, parent_name)
    return activity


@router.get("/{activity_id}/subtree-ids", response_model=list[int])
async def get_activity_subtree(
        activity_id: int,
        db: AsyncSession = Depends(get_db),
) -> list[int]:
    """
    Получение списка ID всех дочерних видов деятельности
    """
    service = get_activity_service(db)
    return await service.get_activity_subtree_ids(activity_id)
