from collections.abc import Sequence
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from main.handlers.users.database.table import Users

from collections.abc import Sequence
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from main.handlers.users.database.table import Users


class CRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, vk_id: int) -> Users:
        db_user = Users(vk_id=vk_id)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def get(self, vk_id: int) -> Users | None:
        return await self.session.get(Users, vk_id)

    async def get_all(self, limit: int = 100, offset: int = 0) -> Sequence[Users]:
        statement = select(Users).offset(offset).limit(limit)
        result = await self.session.exec(statement)
        return result.all()

    async def update(self, vk_id: int, **update_data) -> Users | None:
        db_user = await self.get(vk_id)
        if not db_user:
            return None
        
        for key, value in update_data.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)
                
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def delete(self, vk_id: int) -> bool:
        db_user = await self.get(vk_id)
        if not db_user:
            return False
        await self.session.delete(db_user)
        await self.session.commit()
        return True