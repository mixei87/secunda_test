from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_auth
from src.db.session import db
from src.schemas.activity import ActivityCreate, ActivityOut
from src.services.activity import get_activity_service

router = APIRouter(dependencies=[Depends(get_auth)])


@router.post("/create", response_model=ActivityOut)
async def create_activity(
    activity_data: ActivityCreate, db: AsyncSession = Depends(db)
) -> ActivityOut:
    """
    Создание новой деятельности
    """
    async with db as session:
        service = get_activity_service(session)
        activity = await service.create_activity(
            name=activity_data.name, parent_id=activity_data.parent_id
        )
        return ActivityOut.model_validate(activity)


@router.get("/get_by_name_and_parent_name", response_model=ActivityOut)
async def get_activity_by_name_and_parent_name(
    name: str,
    parent_name: str = "",
    db: AsyncSession = Depends(db),
) -> ActivityOut:
    """
    Получение деятельности по названию и имени родителя
    """
    async with db as session:
        service = get_activity_service(session)
        activity = await service.get_activity_by_name_and_parent_name(name, parent_name)
        if activity is None:
            raise HTTPException(
                status_code=404,
                detail="Деятельность не найдена либо существует несколько записей",
            )
        return ActivityOut.model_validate(activity)


@router.get("/{activity_id}/subtree-ids", response_model=list[int])
async def get_activity_subtree(
    activity_id: int,
    db: AsyncSession = Depends(db),
) -> list[int]:
    """
    Получение списка ID всех дочерних видов деятельности
    """
    async with db as session:
        service = get_activity_service(session)
        return await service.get_activity_subtree_ids(activity_id)
