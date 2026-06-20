from app.src.exceptions.domain_exceptions import DomainEmailVerifiedError

EXCEPTION_MAPPER = {
        DomainEmailVerifiedError           : "Replace with HTTP Exceptions lambda e: DataBaseDataNotFoundException('Entity not found', message=str(e))",

        }   
    