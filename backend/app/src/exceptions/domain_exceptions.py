
class DomainError(Exception):
    """This is the base error for domain."""

    def __init__(self, message='Internal server error. Contact developer if the problem persists.'):
        super().__init__(message)


class DomainEmailNotVerifiedError(DomainError):
    """This is the error when email is not verified and verified."""
    pass

