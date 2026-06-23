from fastapi import APIRouter, BackgroundTasks, Body
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.src.core.constants import ConstantsData
from app.src.core.dependencies import get_email_infrastructure, get_firebase_auth_services, firebase_get_current_user
from app.src.database.models.users import CreateUsers
from app.src.domain.dto.auth_dto import FirebaseGetCurrentUserDTO
from app.src.exceptions.http_exceptions import DataBadRequestException
from app.src.infrastructure.email_infrastructue import EmailInfrastructure
from app.src.schema import EndpointTags, StatusMessage
from app.src.schema.auth_schema import AuthRefreshTokenSchema
from app.src.services.firebase_auth_services import FirebaseAuthServices
from app.src.utils.successful_response import SuccessfulResponse

__base_endpoint = f'{ConstantsData.BASE_ENDPOINT}auth'
v1_auth_router = APIRouter(tags=[EndpointTags.AUTHENTICATION], prefix=__base_endpoint)


@v1_auth_router.post('/signup')
async def firebase_create_account(background_task: BackgroundTasks,
                                  new_user: CreateUsers,
                                  email_infrastructure: EmailInfrastructure = Depends(get_email_infrastructure),
                                  auth_services: FirebaseAuthServices = Depends(get_firebase_auth_services)
                                  ):
    try:
        firebase_auth_response = await auth_services.insert_record(new_user)
        verification_link = firebase_auth_response.data
        if verification_link is not None:
            verification_link = firebase_auth_response.data.get("verification_link")
        # check if there's a verification link

        if firebase_auth_response.status_message == StatusMessage.ALREADY_EXISTS:

            firebase_auth_response.status_code = status.HTTP_200_OK
            return SuccessfulResponse(firebase_auth_response)
        if not verification_link:
            raise DataBadRequestException(
                message="No activation link found, please verify that you specified email.")

        # This is for localhost only
        await email_infrastructure.send_message_via_clicking(
            recipient=new_user.email,
            activation_link=verification_link)
        firebase_auth_response.status_code = status.HTTP_202_ACCEPTED
        response = SuccessfulResponse(firebase_auth_response)

        return response
    except Exception as e:
        print(str(e))
        raise e


@v1_auth_router.post('/login')
async def firebase_authenticate_user(form_data: OAuth2PasswordRequestForm = Depends(),
                                     firebase_authenticate_services: FirebaseAuthServices = Depends(
                                         get_firebase_auth_services)):
    try:
        firebase_auth_response = await firebase_authenticate_services.authenticate_user(form_data.username,
                                                                                        form_data.password)
        firebase_auth_response.status_code = status.HTTP_200_OK

        return SuccessfulResponse(firebase_auth_response)
    except Exception as e:
        print(str(e))
        raise e


@v1_auth_router.post('/refresh-token')
async def firebase_refresh_token(refresh_token:AuthRefreshTokenSchema
                                 ,
                                 firebase_auth_services: FirebaseAuthServices = Depends(get_firebase_auth_services), ):
    try:
        firebase_auth_response = await firebase_auth_services.firebase_refresh_token(refresh_token)
        firebase_auth_response.status_code = status.HTTP_200_OK

        return SuccessfulResponse(firebase_auth_response)
    except Exception as e:
        print(str(e))
        raise e


@v1_auth_router.post('/logout')
async def firebase_logout_user(firebase_auth_services: FirebaseAuthServices = Depends(get_firebase_auth_services),
                               current_user: FirebaseGetCurrentUserDTO = Depends(firebase_get_current_user)):
    try:
        firebase_auth_response = await firebase_auth_services.firebase_logout_user(current_user)
        firebase_auth_response.status_code = status.HTTP_200_OK

        return SuccessfulResponse(firebase_auth_response)
    except Exception as e:
        print(str(e))
        raise e
@v1_auth_router.get('/test')
async def firebase_logout_user(
                               current_user: FirebaseGetCurrentUserDTO = Depends(firebase_get_current_user)):
    print(current_user)