import logging

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from auth.router import router as router_auth
from drive.router import router as router_drive

app = FastAPI()

logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(SessionMiddleware, secret_key="some-random-string")
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(router_auth)
app.include_router(router_drive)
