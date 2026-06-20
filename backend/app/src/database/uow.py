from sqlalchemy.ext.asyncio import AsyncSession

from app.src.database.repositories.user_resopitory import UserRepository


class SQLUnitOfWork:
    def __init__(self, _db: AsyncSession):
        self.__db = _db
        self.user = UserRepository(self.__db)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            await self._db.rollback()
        else:
            await self._db.commit()
        await self._db.close()

