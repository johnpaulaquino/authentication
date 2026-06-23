from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UsersDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str | None = None
    user_id: str | None = None
    user_uid: str  | None= None
    is_email_verified: bool | None = False
    providers: list | None= [] or None
    login_at: datetime | None= None
    created_at: datetime | None= None
    deleted_at: datetime | None = None
