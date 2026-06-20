from typing import Any

from pydantic import BaseModel, Field


class PaginatedSchema(BaseModel):
    skip: int = Field(ge=1, default=1)
    limit: int = Field(ge=10, default=10)

class EndpointTags(str):
    AUTHENTICATION  = "Authentication"
class PaginatedOutput(BaseModel):
    start_page: int
    end_page: int
    total_records: int
    has_next: bool


class SuccessfulResponseSchema(BaseModel):
    message: str
    headers: dict = None
    status_code: int = None
    status_message: str = "ok"
    data: Any = None
    access_token: str = None
    refresh_token: str = None
    csrf_token: str | None = None
    action: str = None
    paginated: PaginatedOutput | None = None
    otp_code: str | None = None
    verification_token: str | None = None
    sign_up_steps: int | None = None
    email: str | None = None


class StatusMessage(str):
    ALREADY_EXISTS = "Already Exists"
    OK = "Ok"
    ERROR="Error"
    FAIL='Fail'