from fastapi import FastAPI

from api.items import router as item_router
from core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(item_router, prefix="/api/v1/items", tags=["Items"])
