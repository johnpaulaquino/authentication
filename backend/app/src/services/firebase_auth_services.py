from hmac import new

import httpx
from firebase_admin import auth

from app.src.core.constants import ConstantsData
from app.src.database.models.users import CreateUsers, CreateUserWithFirebase
from app.src.database.uow import SQLUnitOfWork
from app.src.domain.dto.auth_dto import FirebaseAuthDTO, FirebaseGetCurrentUserDTO
from app.src.exceptions.domain_exceptions import DomainError, DomainEmailNotVerifiedError, \
    DomainInvalidEmailOrPasswordError, DomainInvalidOrExpiredTokenError, DomainUserNotFoundError
from app.src.infrastructure.email_infrastructue import EmailInfrastructure
from app.src.schema import SuccessfulResponseSchema, StatusMessage


class FirebaseAuthServices:
    def __init__(self, uow: SQLUnitOfWork, ):
        self.__uow = uow

    async def insert_record(self, new_user: CreateUsers):
        """
        This is to insert record on firebase and postgresql.
        :param new_user: the data to be inserted.
        :return: Successful response.
        """
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
        """
        This is to authenticate user using the rest api of firebase.
        :param email:
        :param password:
        :return:
        """
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
            if response.status_code != 200:
                raise DomainInvalidEmailOrPasswordError(message="Incorrect email or password.")
            data = FirebaseAuthDTO(**data)
            return SuccessfulResponseSchema(message="Successfully authenticated.",data=data)
        except Exception as e:
            print(str(e))
            raise e

    async def firebase_refresh_token(self, refresh_token: str):
        """
        This function is to refresh the access token using the rest api for firebase.
        :param refresh_token: This is the current refresh token.
        :return: Return the new access and refresh token.
    """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://securetoken.googleapis.com/v1/token?key={ConstantsData.FB_API_KEY}",
                    data={
                        "grant_type": "refresh_token",
                        "refresh_token": refresh_token
                    }
                )

            data = response.json()

            if response.status_code != 200:
                raise DomainInvalidOrExpiredTokenError("Invalid refresh token")
            data = {
                "idToken": data["id_token"],
                "refreshToken": data["refresh_token"],
                "expiresIn": data["expires_in"]
            }
            return FirebaseAuthDTO(**data)
        except Exception as e:
            print(str(e))
            raise e

    async def firebase_logout_user(self,current_user : FirebaseGetCurrentUserDTO):
        """
        This function is to logged out the user using the uid of the current user.
        :param current_user:
        :return:
        """
        try:
            #use the function of the firebase admin.
            auth.revoke_refresh_tokens(current_user.uid)

            return SuccessfulResponseSchema(message="Successfully logged out.")

        except auth.UserNotFoundError as e:
            raise DomainUserNotFoundError("No user found.")
        except Exception as e:
            raise e