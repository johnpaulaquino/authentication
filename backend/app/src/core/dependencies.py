from typing import AsyncGenerator, Any

from fastapi import Depends

from app.src.database import LocalSession
from app.src.database.uow import SQLUnitOfWork
from app.src.infrastructure.email_infrastructue import EmailInfrastructure
from app.src.services.auth_services import AuthServices


def get_email_infrastructure() -> EmailInfrastructure:
    return EmailInfrastructure()


async def get_uow() -> AsyncGenerator[SQLUnitOfWork, Any]:
    async with LocalSession() as session:
        async with SQLUnitOfWork(session) as uow:
            yield uow


def get_auth_services(
        uow: SQLUnitOfWork = Depends(get_uow),
        ) -> AuthServices:
    return AuthServices(uow)