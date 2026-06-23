from fastapi import Body
from pydantic import BaseModel


class AuthRefreshTokenSchema(BaseModel):
    refresh_token: str = Body()