from app.src.exceptions.domain_exceptions import DomainEmailNotVerifiedError
from app.src.exceptions.http_exceptions import DataBadRequestException

EXCEPTION_MAPPER = {
    DomainEmailNotVerifiedError:lambda e: DataBadRequestException("Email not verified",message=str(e)),

}
