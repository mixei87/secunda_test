from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

import src.crud.activity as crud_act
from src.core.config import settings
from src.core.exceptions import NotFoundError, ValidationError, ConflictError
from src.models import Activity


class ActivityService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_activity(
            self, name: str, parent_id: int | None = None
    ) -> Activity:
        if await crud_act.get_activity_by_name_and_parent_id(
                self.session,
                name,
                parent_id
        ):
            raise ConflictError(
                "Деятельность с таким именем и родителем уже существует")

        depth = 1
        if parent_id is not None:
            parent = await crud_act.get_activity_by_id(self.session, parent_id)
            if parent is None:
                raise NotFoundError(f"Деятельность с ID {parent_id} не найдена")
            if parent.depth >= settings.ACTIVITY_MAX_DEPTH:
                raise ValidationError(
                    f"Превышена максимальная глубина вложенности: {settings.ACTIVITY_MAX_DEPTH}"
                )
            depth = parent.depth + 1

        return await crud_act.create_activity(
            self.session, name=name, parent_id=parent_id, depth=depth
        )

    async def get_activity_by_name_and_parent_name(
            self, name: str, parent_name: str | None = None
    ) -> Activity:
        """Найти деятельность по имени и имени родителя.

        Args:
            name: Название деятельности
            parent_name: Название родительской деятельности (опционально)

        Returns:
            Activity если найдена ровно одна деятельность, иначе None

        Note:
            - Если parent_name не указан, ищется деятельность без родителя
            - Если parent_name указан, сначала ищется родитель с таким именем,
              затем ищется дочерняя деятельность с указанным именем
        """
        # Если указано имя родителя, находим его ID
        parent_id = None
        if parent_name is not None:
            parent = await crud_act.get_parent_activity_by_name(self.session,
                                                                parent_name)
            if parent is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Родительская деятельность с именем '{parent_name}' не найдена"
                )
            parent_id = parent.id

        # Ищем деятельность по имени и ID родителя
        activity = await crud_act.get_activity_by_name_and_parent_id(
            self.session, name=name, parent_id=parent_id
        )

        if activity is None:
            raise HTTPException(
                status_code=404,
                detail=f"Деятельность с именем {name} с родителем {parent_id} не найдена"
            )
        return activity

    async def get_activity_subtree_ids(self, activity_id: int) -> list[int]:
        """Получить список ID всех дочерних видов деятельности"""
        if await crud_act.get_activity_by_id(self.session, activity_id) is None:
            raise NotFoundError(f"Деятельность с ID {activity_id} не найдена")
        return await crud_act.subtree_ids(self.session, activity_id)


def get_activity_service(session: AsyncSession) -> ActivityService:
    return ActivityService(session)
