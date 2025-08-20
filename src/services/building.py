from sqlalchemy.ext.asyncio import AsyncSession

import src.crud.building as crud

from src.models.building import Building


class BuildingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_building(
        self, address: str, latitude: float, longitude: float
    ) -> Building:
        """Создать новое здание"""
        return await crud.create_building(self.db, address, latitude, longitude)

    async def get_building_by_id(self, building_id: int) -> Building | None:
        """Получить здание по ID"""
        return await crud.get_building_by_id(self.db, building_id)

    async def get_building_by_address(self, address: str) -> Building | None:
        """Получить здание по адресу"""
        return await crud.get_building_by_address(self.db, address)

    async def list_buildings(
        self, q: str = "", limit: int = 15, offset: int = 0
    ) -> list[Building]:
        """Получить список зданий"""
        return await crud.list_buildings(self.db, q=q, limit=limit, offset=offset)

    async def get_or_create_building(
        self, address: str, latitude: float, longitude: float
    ) -> tuple[bool, Building]:
        """Получить или создать здание"""
        if building := await self.get_building_by_address(address):
            return False, building
        return True, await self.create_building(address, latitude, longitude)


def get_building_service(session: AsyncSession) -> BuildingService:
    return BuildingService(session)
