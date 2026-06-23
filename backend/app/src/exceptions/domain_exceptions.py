
class DomainError(Exception):
    """This is the base error for domain."""

    def __init__(self, message='Internal server error. Contact developer if the problem persists.'):
        super().__init__(message)


class DomainEmailNotVerifiedError(DomainError):
    """This is the error when email is not verified and verified."""
    pass

class DomainInvalidEmailOrPasswordError(DomainError):
    """This is the error when email or password is not valid."""
    pass


class DomainInvalidOrExpiredTokenError(DomainError):
    """This is the error when token is expired or invalid."""
    pass

class DomainUserNotFoundError(DomainError):
    """This is the error when user is not found."""
    pass