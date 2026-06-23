from pydantic import BaseModel


class FirebaseAuthDTO(BaseModel):
    idToken : str | None = None
    refreshToken : str | None = None
    expiresIn: str | None = None


class FirebaseGetCurrentUserDTO(BaseModel):
    email: str
    uid : str