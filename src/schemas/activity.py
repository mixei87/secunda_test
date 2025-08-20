from pydantic import BaseModel, Field


class ActivityCreate(BaseModel):
    """Данные для создания новой деятельности"""

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Название деятельности. Должно содержать от 1 до 255 символов",
    )

    parent_id: int | None = Field(
        None,
        gt=0,
        le=2_147_483_647,
        description="ID родительской деятельности. Должен быть положительным числом не более 2147483647",
    )


class ActivityOut(BaseModel):
    id: int
    name: str
    parent_id: int | None
    depth: int

    class Config:
        from_attributes = True


class ActivityNode(ActivityOut):
    children: list["ActivityNode"] | None = None
