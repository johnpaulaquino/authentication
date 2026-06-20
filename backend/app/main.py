
import sys
from fastapi import FastAPI
import uvicorn

from app.src.core.constants import ConstantsData
from app.src.utils import app_life_span

app = FastAPI(lifespan=app_life_span)




def start():
    """Entry point for the 'server' command in pyproject.toml"""
    use_loop = "uvloop" if sys.platform != "win32" else "auto"  # to avoid conflict in windows.
    uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=ConstantsData.SERVER_PORT,
            workers=4,
            loop=use_loop,  # use uv loop for faster
            proxy_headers=True,
            forwarded_allow_ips="*", )


if __name__ == "__main__":
    # start the server
    start()
