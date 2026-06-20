from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.database.models import Users
from app.src.database.models.users import CreateUsers
from app.src.domain.dto.users_dto import UsersDto
from app.src.domain.interface.repository_interface import RepositoryInterface


class UserRepository(RepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def insert_record(self, record: CreateUsers):
        try:
            user = Users(**record.model_dump())
            self.__db.add(user)
        except Exception as e:
            print(str(e))
            raise e

    async def find_record(self, record_id: str) -> UsersDto:
       try:
           stmt = select(Users).where(Users.user_uid == record_id)
           result = await self.__db.execute(stmt)
           data = result.scalar()
           return data
       except Exception as e:
           print(str(e))
           raise e

    async def update_record(self, record_id: str, data: dict | None = None):
        try:
            pass
        except Exception as e:
            print(str(e))
            raise e

    async def delete_record(self, record_id: str):
        try:
            pass
        except Exception as e:
            print(str(e))
            raise e

    async def soft_delete_record(self, record_id: str) -> None:
        try:
            pass
        except Exception as e:
            print(str(e))
            raise e