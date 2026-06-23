from app.src.exceptions.domain_exceptions import DomainEmailNotVerifiedError, DomainInvalidEmailOrPasswordError, \
    DomainInvalidOrExpiredTokenError, DomainUserNotFoundError
from app.src.exceptions.http_exceptions import DataBadRequestException, JWTExpiredException, \
    DataBaseDataNotFoundException

EXCEPTION_MAPPER = {
    DomainEmailNotVerifiedError: lambda e: DataBadRequestException("EMAIL_NOT_VERIFIED", message=str(e)),
    DomainInvalidEmailOrPasswordError: lambda e: DataBadRequestException('INCORRECT_CREDENTIALS',
                                                                         message=str(e), ),
    DomainInvalidOrExpiredTokenError: lambda e: JWTExpiredException('EXPIRED_OR_INVALID',
                                                                         message=str(e) ),
    DomainUserNotFoundError : lambda e: DataBaseDataNotFoundException('USER_NOT_FOUND',message=str(e))
}
