from fastapi import APIRouter, BackgroundTasks
from fastapi.params import Depends
from starlette import status

from app.src.core.constants import ConstantsData
from app.src.core.dependencies import get_email_infrastructure, get_auth_services
from app.src.database.models.users import CreateUsers
from app.src.exceptions.http_exceptions import DataBadRequestException
from app.src.infrastructure.email_infrastructue import EmailInfrastructure
from app.src.schema import EndpointTags, StatusMessage
from app.src.services.auth_services import AuthServices
from app.src.utils.successful_response import SuccessfulResponse

__base_endpoint = f'{ConstantsData.BASE_ENDPOINT}auth'
v1_auth_router = APIRouter(tags=[EndpointTags.AUTHENTICATION], prefix=__base_endpoint)


@v1_auth_router.post('/signup')
async def create_account(background_task: BackgroundTasks,
                         new_user : CreateUsers,
                         email_infrastructure: EmailInfrastructure = Depends(get_email_infrastructure),
                         auth_services: AuthServices = Depends(get_auth_services)
                         ):
    try:
        auth_response = await auth_services.insert_record(new_user)
        verification_link = auth_response.data
        if verification_link is not None:
            verification_link =  auth_response.data.get("verification_link")
        #check if there's a verification link

        if auth_response.status_message == StatusMessage.ALREADY_EXISTS:

            auth_response.status_code = status.HTTP_200_OK
            return SuccessfulResponse(auth_response)
        if not verification_link:
            raise DataBadRequestException(message="No activation link found, please verify that you specified email.")

        await email_infrastructure.send_message_via_clicking(
                recipient=new_user.email,
                activation_link=verification_link)
        auth_response.status_code = status.HTTP_202_ACCEPTED
        response = SuccessfulResponse(auth_response)

        return response
    except Exception as e:
        print(str(e))
        raise e
@v1_auth_router.post('/login')
async def authenticate_user(email : str, password : str,
                            authenticate_services : AuthServices = Depends(get_auth_services)):
    try:
        auth_response = await authenticate_services.authenticate_user(email, password)
        auth_response.status_code = status.HTTP_200_OK

        return SuccessfulResponse(auth_response)
    except Exception as e:
        print(str(e))
        raise e