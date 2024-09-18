from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.tasks_router import router as task_router
from api.user_router import router as user_router

from database.init_db import init_db
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info('Intialization of DB has been started!')
    await init_db()
    yield
    logging.info('Done!')

def application_factory() -> FastAPI:

    app = FastAPI(lifespan=lifespan)

    app.include_router(user_router)
    app.include_router(task_router)

    return app

app = application_factory()