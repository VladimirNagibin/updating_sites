import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.api_test import test_router
from api.v1.update_portal import upd_portal
from api.v1.upload_file import upload_file_router
from core.logger import LOGGING
from core.settings import settings

# from db.elastic import elastic
# from db.redis import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # redis.redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    # FastAPICache.init(RedisBackend(redis.redis), prefix="fastapi-cache")
    # elastic.es = AsyncElasticsearch(
    #    hosts=[f"{settings.ELASTIC_SCHEME}://{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}"]
    # )
    yield

    # await redis.redis.close()
    # await elastic.es.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(upload_file_router, prefix="/api/v1/files", tags=["files"])
app.include_router(upd_portal, prefix="/api/v1/update", tags=["update"])
app.include_router(test_router, prefix="/api/v1/tests", tags=["tests"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=settings.APP_RELOAD,
    )
