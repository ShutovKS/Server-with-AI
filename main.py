import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routers import api_router
from app.settings import init_settings

load_dotenv()

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

app = FastAPI()

init_settings()

app.include_router(api_router, prefix="/api")


def mount_static(directory: str, path: str):
    if os.path.exists(directory):
        app.mount(path, StaticFiles(directory=directory), name=directory)


mount_static("storage", "/api/files/data")
mount_static("output", "/api/files/output")

if __name__ == "__main__":
    uvicorn.run("main:app", host=APP_HOST, port=APP_PORT, reload=True)
