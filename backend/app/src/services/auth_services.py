from hmac import new

from firebase_admin import auth

from app.src.database.models.users import CreateUsers
from app.src.database.uow import SQLUnitOfWork
from app.src.exceptions.domain_exceptions import DomainError, DomainEmailNotVerifiedError
from app.src.schema import SuccessfulResponseSchema


class AuthServices:
    def __init__(self,uow : SQLUnitOfWork):
        self.__uow = uow


    async def insert_record(self,new_user : CreateUsers):
        try:
            data = await self.__uow.user.find_record(new_user.email)
            if data:
                #check if email is verified
                if data.is_email_verified:
                    return SuccessfulResponseSchema(message="Email already verified. Please proceed to login instead.")

                raise DomainEmailNotVerifiedError("Email not verified. Please verify your email.")


        #generate verification link
            verification_link = auth.generate_email_verification_link(new_user.email)



        except Exception as e:
            print(str(e))
            raise e