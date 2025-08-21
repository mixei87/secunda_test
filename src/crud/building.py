from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.building import Building


async def create_building(
    session: AsyncSession, address: str, latitude: float, longitude: float
) -> Building:
    """Создать новое здание"""
    building = Building(address=address, latitude=latitude, longitude=longitude)
    session.add(building)
    await session.flush()
    return building


async def get_building_by_id(
    session: AsyncSession, building_id: int
) -> Building | None:
    """Получить здание по ID"""
    result = await session.execute(select(Building).filter(Building.id == building_id))
    return result.scalar_one_or_none()


async def get_building_by_address(
    session: AsyncSession, address: str
) -> Building | None:
    """Получить здание по адресу"""
    result = await session.execute(select(Building).where(Building.address == address))
    return result.scalar_one_or_none()


async def list_buildings(
    session: AsyncSession, q: str = "", limit: int = 15, offset: int = 0
):
    stmt = select(Building)
    if q:
        stmt = stmt.where(Building.address.ilike(f"%{q}%"))
    stmt = stmt.limit(limit).offset(offset)
    result = await session.execute(stmt)
    return result.scalars().all()
