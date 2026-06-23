from typing import AsyncGenerator, Any

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth

from app.src.database import LocalSession
from app.src.database.uow import SQLUnitOfWork
from app.src.domain.dto.auth_dto import FirebaseGetCurrentUserDTO
from app.src.exceptions.domain_exceptions import DomainInvalidOrExpiredTokenError
from app.src.infrastructure.email_infrastructue import EmailInfrastructure
from app.src.services.firebase_auth_services import FirebaseAuthServices


security = HTTPBearer()


async def firebase_get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)) -> FirebaseGetCurrentUserDTO:
    """
    This function will use for dependency to make the route protected.This dependency is firebase provider.
    :param credentials: This is the authorization credential.
    :return: The decoded token.
    """
    try:
        token = credentials.credentials

        decoded_token = auth.verify_id_token(token)

        return FirebaseGetCurrentUserDTO(**decoded_token)

    except Exception:
        raise DomainInvalidOrExpiredTokenError("Your token is invalid or expired.")


def get_email_infrastructure() -> EmailInfrastructure:
    return EmailInfrastructure()


async def get_uow() -> AsyncGenerator[SQLUnitOfWork, Any]:
    async with LocalSession() as session:
        async with SQLUnitOfWork(session) as uow:
            yield uow


def get_firebase_auth_services(
        uow: SQLUnitOfWork = Depends(get_uow),
) -> FirebaseAuthServices:
    return FirebaseAuthServices(uow)

