from sqlalchemy import Integer, String, Float, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base


class Building(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    address: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    organizations = relationship("Organization", back_populates="building", lazy="selectin")


Index("ix_building_lat_lon", Building.latitude, Building.longitude)
