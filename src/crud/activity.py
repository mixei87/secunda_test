from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.activity import Activity


async def create_activity(
    session: AsyncSession, name: str, parent_id: int | None = None, depth: int = 1
) -> Activity:
    activity = Activity(name=name, parent_id=parent_id, depth=depth)
    session.add(activity)
    await session.flush()
    return activity


async def get_activity_by_id(
    session: AsyncSession, activity_id: int
) -> Activity | None:
    """Найти деятельность по ID.

    Args:
        session: Сессия БД
        activity_id: ID деятельности

    Returns:
        Activity если найдена ровно одна деятельность, иначе None
    """
    result = await session.execute(select(Activity).filter(Activity.id == activity_id))
    return result.scalar_one_or_none()


async def get_activity_by_name(session: AsyncSession, name: str) -> Activity | None:
    """Найти деятельность по имени.

    Args:
        session: Сессия БД
        name: Название деятельности

    Returns:
        Activity если найдена ровно одна деятельность, иначе None
    """
    result = await session.execute(select(Activity).where(Activity.name.ilike(name)))
    return result.scalar_one_or_none()


async def get_activity_by_name_and_parent_id(
    session: AsyncSession, name: str, parent_id: int | None = None
) -> Activity | None:
    """Найти деятельность по имени и по parent_id.

    Args:
        session: Сессия БД
        name: Название деятельности
        parent_id: ID родительской деятельности

    Returns:
        Activity если найдена ровно одна деятельность, иначе None
    """
    stmt = select(Activity).where(Activity.name.ilike(name))

    if parent_id is None:
        stmt = stmt.where(Activity.parent_id.is_(None))
    else:
        stmt = stmt.where(Activity.parent_id == parent_id)

    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_children(session: AsyncSession, activity_id: int) -> list[int]:
    result = await session.execute(
        select(Activity.id).where(Activity.parent_id == activity_id)
    )
    return list(result.scalars().all())


async def subtree_ids(session: AsyncSession, activity_id: int) -> list[int]:
    """Возвращает список ID всех дочерних элементов рекурсивно."""
    result = [activity_id]
    children_ids = await get_children(session, activity_id)
    for child_id in children_ids:
        result.extend(await subtree_ids(session, child_id))
    return result
