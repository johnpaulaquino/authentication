from hmac import new

import httpx
from firebase_admin import auth

from app.src.core.constants import ConstantsData
from app.src.database.models.users import CreateUsers, CreateUserWithFirebase
from app.src.database.uow import SQLUnitOfWork
from app.src.exceptions.domain_exceptions import DomainError, DomainEmailNotVerifiedError, \
    DomainInvalidEmailOrPasswordError
from app.src.infrastructure.email_infrastructue import EmailInfrastructure
from app.src.schema import SuccessfulResponseSchema, StatusMessage


class AuthServices:
    def __init__(self, uow: SQLUnitOfWork, ):
        self.__uow = uow

    async def insert_record(self, new_user: CreateUsers):
        try:
            try:
                firebase_user = auth.get_user_by_email(new_user.email)
            except Exception as e:
                print(str(e))
                firebase_user = None


            #check in database if user exists
            data = await self.__uow.user.find_record(new_user.email)

            if data:
                #check if the email is verified
                if firebase_user.email_verified:
                    #then update is email verified in database
                    data_to_update = {"is_email_verified" : True}
                    await self.__uow.user.update_record(new_user.email,data_to_update)
                    return SuccessfulResponseSchema(message="Email already verified. Please proceed to login instead.",status_message=StatusMessage.ALREADY_EXISTS)

                # check if email is verified
                if data.is_email_verified:
                    return SuccessfulResponseSchema(message="Email already verified. Please proceed to login instead.",status_message=StatusMessage.ALREADY_EXISTS)

                raise DomainEmailNotVerifiedError("Email not verified. Please verify your email.")

            #otherwise create account for firebase
            firebase_user = auth.create_user(
                email=new_user.email,
                password=new_user.password
            )
            #create account in database
            new_record = CreateUserWithFirebase(email=new_user.email,user_uid=firebase_user.uid)

            #insert data into postgresql
            await self.__uow.user.insert_record(new_record)
            # generate verification link
            verification_link = auth.generate_email_verification_link(firebase_user.email)

            #return the successful response
            return SuccessfulResponseSchema(
                message="Please verify your account. We already sent your activation account in your email.",
                data={"verification_link": verification_link})
        except Exception as e:
            print(str(e))
            raise e

    async def authenticate_user(self, email: str, password: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={ConstantsData.FB_API_KEY}",
                    json={
                        "email": email,
                        "password": password,
                        "returnSecureToken": True
                    }
                )

            data = response.json()
            print(data)

            if response.status_code != 200:
                print(response)
                raise DomainInvalidEmailOrPasswordError(message="Incorrect email or password")

            return SuccessfulResponseSchema(message="Successfully authenticated.",data=data)
        except Exception as e:
            print(str(e))
            raise e
