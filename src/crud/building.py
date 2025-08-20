from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.building import Building


async def create_building(
    db: AsyncSession, address: str, latitude: float, longitude: float
) -> Building:
    """Создать новое здание"""
    building = Building(address=address, latitude=latitude, longitude=longitude)
    db.add(building)
    await db.flush()
    return building


async def get_building_by_id(db: AsyncSession, building_id: int) -> Building | None:
    """Получить здание по ID"""
    result = await db.execute(select(Building).filter(Building.id == building_id))
    return result.scalar_one_or_none()


async def get_building_by_address(db: AsyncSession, address: str) -> Building | None:
    """Получить здание по адресу"""
    result = await db.execute(select(Building).where(Building.address == address))
    return result.scalar_one_or_none()


async def list_buildings(
    db: AsyncSession, q: str = "", limit: int = 15, offset: int = 0
):
    stmt = select(Building)
    if q:
        stmt = stmt.where(Building.address.ilike(f"%{q}%"))
    stmt = stmt.limit(limit).offset(offset)
    result = await db.execute(stmt)
    return result.scalars().all()
