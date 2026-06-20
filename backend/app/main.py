import sys
from fastapi import FastAPI
import uvicorn

from app.src.api.v1.auth_route import v1_auth_router
from app.src.core.constants import ConstantsData
from app.src.exceptions import app_exception_handler, BaseAppExceptions
from app.src.exceptions.domain_exceptions import DomainError
from app.src.utils import app_life_span

app = FastAPI(lifespan=app_life_span)

# to handle custom exception
app.add_exception_handler(handler=app_exception_handler,
                          exc_class_or_status_code=BaseAppExceptions)
app.add_exception_handler(handler=app_exception_handler,
                          exc_class_or_status_code=DomainError)
app.add_exception_handler(handler=app_exception_handler,
                          exc_class_or_status_code=Exception)

app.include_router(v1_auth_router)


def start():
    """Entry point for the 'server' command in pyproject.toml"""
    use_loop = "uvloop" if sys.platform != "win32" else "auto"  # to avoid conflict in windows.
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=ConstantsData.SERVER_PORT,
        reload=True,
        workers=4,
        loop=use_loop,  # use uv loop for faster
        proxy_headers=True,
        forwarded_allow_ips="*", )


if __name__ == "__main__":
    # start the server
    start()
