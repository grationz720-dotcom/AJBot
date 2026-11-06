from sqlmodel import Field, SQLModel

class Users(SQLModel, table=True): # type: ignore
    vk_id: int = Field(
        nullable=False,
        primary_key=True,
        description="VK ID пользователя - используется вместо классического id."
    )