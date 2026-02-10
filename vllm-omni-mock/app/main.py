from fastapi import FastAPI

from .routers import v1_images

app = FastAPI()

app.include_router(v1_images.router)
