from pydantic import BaseModel, Field


class BuildingBase(BaseModel):
    address: str = Field(...)
    latitude: float
    longitude: float


class BuildingOut(BuildingBase):
    id: int

    class Config:
        from_attributes = True
