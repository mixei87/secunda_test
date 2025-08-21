import asyncio
from typing import Any

from src.db.session import get_db
from src.services.building import get_building_service, BuildingService

from src.services.activity import get_activity_service, ActivityService

# from src.services.organization import get_organization_service


# Данные для заполнения
BUILDINGS = [
    {"address": "г. Москва, ул. Ленина 1, офис 3", "lat": 55.7558, "lon": 37.6173},
    {"address": "г. Москва, ул. Тверская 10", "lat": 55.7658, "lon": 37.6050},
    {"address": "г. Москва, пр-т Мира 50", "lat": 55.7900, "lon": 37.6340},
    {"address": "г. Санкт-Петербург, Невский пр., 20", "lat": 59.9343, "lon": 30.3351},
    {"address": "г. Санкт-Петербург, Литейный пр., 15", "lat": 59.9390, "lon": 30.3500},
    {"address": "г. Новосибирск, ул. Блюхера 32/1", "lat": 55.0415, "lon": 82.9346},
    {"address": "г. Екатеринбург, ул. Мира 12", "lat": 56.8389, "lon": 60.6057},
    {"address": "г. Казань, ул. Баумана 5", "lat": 55.7903, "lon": 49.1347},
]

ACTIVITIES = [
    {"name": "Еда", "parent": None},
    {"name": "Фастфуд", "parent": "Еда"},
    {"name": "Рестораны", "parent": "Еда"},
    {"name": "Услуги", "parent": None},
    {"name": "Медицина", "parent": "Услуги"},
    {"name": "Финансы", "parent": "Услуги"},
    {"name": "Розничная торговля", "parent": None},
]


#
# ORGANIZATIONS = [
#     {"name": "Вкусно и точка", "building_idx": 0, "phones": ["+79161234567"]},
#     {"name": "Прачечная №1", "building_idx": 1, "phones": ["+79161234568"]},
#     {"name": "Аптека 36.6", "building_idx": 2, "phones": ["+79161234569"]},
#     {"name": "Сбербанк", "building_idx": 3, "phones": ["+79161234570"]},
#     {"name": "Пятерочка", "building_idx": 4, "phones": ["+79161234571"]},
#     {"name": "Магнит", "building_idx": 5, "phones": ["+79161234572"]},
#     {"name": "Лента", "building_idx": 6, "phones": ["+79161234573"]},
#     {"name": "Метро", "building_idx": 7, "phones": ["+79161234574"]},
# ]
#
#
# # Связи организаций с видами деятельности
# ORG_ACTIVITIES = {
#     "Вкусно и точка": ["Фастфуд"],
#     "Прачечная №1": ["Услуги"],
#     "Аптека 36.6": ["Медицина"],
#     "Сбербанк": ["Финансы"],
#     "Пятерочка": ["Розничная торговля"],
#     "Магнит": ["Розничная торговля"],
#     "Лента": ["Розничная торговля"],
#     "Метро": ["Розничная торговля"],
# }


def log_creation(entity_type: str, entity: Any, created: bool):
    """Логирование создания/получения сущности"""
    status = "создано" if created else "найдено"
    print(f"{entity_type.capitalize()} {status}: {entity}")


async def seed_buildings(building_service: BuildingService):
    """Заполнение зданий"""
    print("\n=== Заполнение зданий ===")
    for building_data in BUILDINGS:
        created, building = await building_service.get_or_create_building(
            address=building_data["address"],
            latitude=building_data["lat"],
            longitude=building_data["lon"],
        )
        log_creation("здание", building.address, created)


async def seed_activities(service: ActivityService):
    """Заполнение видов деятельности"""
    print("\n=== Заполнение видов деятельности ===")
    activity_map = {}

    for activity_data in ACTIVITIES:
        parent = (
            activity_map.get(activity_data["parent"])
            if activity_data["parent"]
            else None
        )
        created, activity = await service.get_or_create_activity(
            name=activity_data["name"], parent=parent, depth=activity_data["depth"]
        )
        activity_map[activity.name] = activity
        log_creation("вид деятельности", activity.name, created)


#
#
# async def seed_organizations(building_service, org_service, activity_service):
#     """Заполнение организаций"""
#     print("\n=== Заполнение организаций ===")
#
#     # Получаем все здания для связей
#     buildings = await building_service.list_buildings(limit=100)
#
#     for org_data in ORGANIZATIONS:
#         # Получаем здание по индексу
#         building = buildings[org_data["building_idx"]]
#
#         # Создаем или получаем организацию
#         created, org = await org_service.get_or_create_organization(
#             name=org_data["name"], building_id=building.id
#         )
#         log_creation("организация", org.name, created)
#
#         # Добавляем телефоны
#         for phone in org_data["phones"]:
#             await org_service.add_phone(org.id, phone)
#
#         # Добавляем виды деятельности
#         for activity_name in ORG_ACTIVITIES.get(org_data["name"], []):
#             activity = await activity_service.get_activity_by_name(activity_name)
#             if activity:
#                 await org_service.add_activity(org.id, activity.id)


async def main():
    """Основная функция заполнения данных"""
    async with get_db() as session:
        # Инициализируем сервисы
        building_service = get_building_service(session)
        activity_service = get_activity_service(session)
        # org_service = get_organization_service(session)

        # Заполняем данные
        await seed_buildings(building_service)
        await seed_activities(activity_service)
        # await seed_organizations(building_service, org_service, activity_service)

        print("\n=== Заполнение данных завершено успешно ===")


if __name__ == "__main__":
    asyncio.run(main())
