from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.routers import v1_router
from src.configurations.database import global_init, create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    global_init()
    await create_db_and_tables()
    yield

app = FastAPI(
    title="Book Library App",
    description="Учебное приложение для MTS Shad",
    version="0.0.1",
    default_response_class=ORJSONResponse,
    responses={404: {"description": "Not Found!"}},
    lifespan=lifespan,
)

app.include_router(v1_router)
