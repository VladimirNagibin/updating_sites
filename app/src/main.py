import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

#from api.v1 import films
#from api.v1.genres import genres
#from api.v1.persons import persons
#from core.settings import settings
#from core.logger import LOGGING
#from db.elastic import elastic
#from db.redis import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    #redis.redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    #FastAPICache.init(RedisBackend(redis.redis), prefix="fastapi-cache")
    #elastic.es = AsyncElasticsearch(
    #    hosts=[f"{settings.ELASTIC_SCHEME}://{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}"]
    #)
    yield

    #await redis.redis.close()
    #await elastic.es.close()


app = FastAPI(
    title='settings.PROJECT_NAME',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

#app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
#app.include_router(genres, prefix="/api/v1/genres", tags=["genres"])
#app.include_router(persons, prefix="/api/v1/persons", tags=["persons"])


@app.get("/")
async def home():
    return {"data": "Hello World5555"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        #log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True, #settings.APP_RELOAD,
    )
