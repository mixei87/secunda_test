from sqlalchemy.ext.asyncio import AsyncSession

import src.crud.activity as crud
from src.core.config import settings
from src.core.exceptions import NotFoundError, ValidationError
from src.models.activity import Activity


class ActivityService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_activity(
        self, name: str, parent_id: int | None = None
    ) -> Activity:
        depth = 1
        if parent_id is not None:
            parent = await crud.get_activity_by_id(self.session, parent_id)
            if parent is None:
                raise NotFoundError(f"Деятельность с ID {parent_id} не найдена")
            if parent.depth >= settings.ACTIVITY_MAX_DEPTH:
                raise ValidationError(
                    f"Превышена максимальная глубина вложенности: {settings.ACTIVITY_MAX_DEPTH}"
                )
            depth = parent.depth + 1

        return await crud.create_activity(
            self.session, name=name, parent_id=parent_id, depth=depth
        )

    async def get_activity_by_name_and_parent_name(
        self, name: str, parent_name: str = ""
    ) -> Activity | None:
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
        parent = None
        if parent_name:
            parent = await crud.get_activity_by_name(self.session, name=parent_name)
            if parent is None:
                return None

        return await crud.get_activity_by_name_and_parent_id(
            self.session, name=name, parent_id=parent.id if parent else None
        )

    async def get_activity_subtree_ids(self, activity_id: int) -> list[int]:
        """Получить список ID всех дочерних видов деятельности"""
        if await crud.get_activity_by_id(self.session, activity_id) is None:
            raise NotFoundError(f"Деятельность с ID {activity_id} не найдена")
        return await crud.subtree_ids(self.session, activity_id)


def get_activity_service(session: AsyncSession) -> ActivityService:
    return ActivityService(session)
