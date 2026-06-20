import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Constants(BaseSettings):
    ENVIRONMENT: str
    # this is for database
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int

    #Base endpoint name
    BASE_ENDPOINT : str = "/api/v1/project/"

    #email
    MAIL_USERNAME: str
    MAIL_PASSWORD: SecretStr
    MAIL_FROM: str | EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    MAIL_USE_CREDENTIALS: bool
    MAIL_VALIDATE_CERTS: bool

    SERVER_PORT: int

    #production_env
    DB_PROD_USER :str
    DB_PROD_HOST : str
    DB_PROD_NAME : str
    DB_PROD_PORT : int
    DB_PROD_PASSWORD : str

    #firebase configuration
    FB_API_KEY : str
    FB_PRIVATE_KEY_ID :str
    FB_PROJECT_ID: str
    FB_PRIVATE_KEY : str
    FB_CLIENT_EMAIL : str
    FB_CLIENT_ID : str
    FB_AUTH_URI :str
    FB_TOKEN_URI :str
    FB_AUTH_PROVIDER_CERT_URL :str
    FB_CLIENT_CERT_URL : str
    FB_UNIVERSE_DOMAIN : str

    TEMPLATE_PATH: Path = Path(__file__).resolve().parent

    FILE_SIZE_LIMIT: int = 1024 * 1024 * 10  # it is exactly 10 mb

    STATIC_PATH: str = os.path.abspath(os.path.join(os.curdir, 'static'))

    # for prefix in http

    model_config = SettingsConfigDict(
            env_file='../../../.example.env'
            )

class EnvironmentStatus(str):
    DEVELOPMENT ="Dev"
    PRODUCTION  = "Production"
    TESTING = "Testing"


ConstantsData = Constants()
