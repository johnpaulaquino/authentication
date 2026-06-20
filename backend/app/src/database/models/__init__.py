from sqlmodel import SQLModel

from app.src.database.models.users import Users

BaseSQLModel = SQLModel()

__all__ = ["Users"]