from datetime import date, datetime
from uuid import uuid4

from sqlalchemy import Column, Date, DateTime, ARRAY, String, func
from sqlmodel import SQLModel, Field


class BaseUsers(SQLModel):
    email : str = Field(unique=True, nullable=True)


class Users(BaseUsers, table=True):
    __tablename__ = "users"
    user_id : str = Field(default_factory=lambda : str(uuid4()),primary_key=True)
    user_uid: str = Field(unique=True)
    is_email_verified : bool = Field(default=False)
    providers  : list = Field(default_factory=lambda : ['email'],
                              sa_column=Column(ARRAY(String)))
    login_at : datetime = Field(sa_column=Column(DateTime(timezone=True),nullable=True))
    created_at : datetime = Field(sa_column=Column(DateTime(timezone=True),nullable=True,
                                                   default=func.now(),
                                                   server_default=func.now()))
    deleted_at : datetime = Field(sa_column=Column(DateTime(timezone=True),nullable=True))


class CreateUsers(BaseUsers):
    password: str = Field(nullable=True)

class CreateUserWithFirebase(SQLModel):
    email : str = Field(unique=True, nullable=True)
    user_uid: str = Field(unique=True)
