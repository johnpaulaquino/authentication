from app.src.core.constants import ConstantsData
from fastapi_mail import ConnectionConfig

#firebase config
FIREBASE_CONFIG : dict = {
    "type": "service_account",
    "project_id": ConstantsData.FB_PROJECT_ID,
    "private_key_id": ConstantsData.FB_PRIVATE_KEY_ID,
    "private_key": ConstantsData.FB_PRIVATE_KEY.replace("\\n", "\n"),
    "client_email": ConstantsData.FB_CLIENT_EMAIL,
    "client_id": ConstantsData.FB_CLIENT_ID,
    "auth_uri": ConstantsData.FB_AUTH_URI,
    "token_uri": ConstantsData.FB_TOKEN_URI,
    "auth_provider_x509_cert_url": ConstantsData.FB_AUTH_PROVIDER_CERT_URL,
    "client_x509_cert_url": ConstantsData.FB_CLIENT_CERT_URL,
    "universe_domain": ConstantsData.FB_UNIVERSE_DOMAIN
}

#email configuration

MAIL_CONFIGURATION = ConnectionConfig(
        MAIL_USERNAME=ConstantsData.MAIL_USERNAME,
        MAIL_PASSWORD=ConstantsData.MAIL_PASSWORD,
        MAIL_FROM=ConstantsData.MAIL_FROM,
        MAIL_PORT=ConstantsData.MAIL_PORT,
        MAIL_SERVER=ConstantsData.MAIL_SERVER,
        MAIL_STARTTLS=ConstantsData.MAIL_STARTTLS,
        MAIL_SSL_TLS=ConstantsData.MAIL_SSL_TLS,
        USE_CREDENTIALS=ConstantsData.MAIL_USE_CREDENTIALS,
        VALIDATE_CERTS=ConstantsData.MAIL_VALIDATE_CERTS,
        TEMPLATE_FOLDER=ConstantsData.TEMPLATE_PATH.parent.parent / 'templates' / 'email',
        )
RESEND_TEMPLATE_PATH=ConstantsData.TEMPLATE_PATH.parent.parent / 'templates' / 'email'