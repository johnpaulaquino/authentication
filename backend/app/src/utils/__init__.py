from contextlib import asynccontextmanager

import firebase_admin
from dotenv import load_dotenv
from fastapi import FastAPI
from firebase_admin import credentials

from app.config import FIREBASE_CONFIG
from app.src.core.constants import ConstantsData




load_dotenv()
@asynccontextmanager
async def app_life_span(app : FastAPI):
    print(f"Server is running at port {ConstantsData.SERVER_PORT}")

    #Run firebase Admin
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_CONFIG)

        firebase_admin.initialize_app(cred)

    yield
    print(f'Server is shutting down.')