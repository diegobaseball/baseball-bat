from config import VERSION, DEBUG, SERVER_HOST, SERVER_PORT
from apps.db import lifespan
from apis import router
from fastapi import FastAPI
from uvicorn import run


app = FastAPI(
    title="Korea baseball Backend",
    version=VERSION,
    debug=DEBUG,
    openapi_url="/admin/openapi.json",
    docs_url="/admin/docs",
    redoc_url="/admin/redoc",
    lifespan=lifespan,
)


if __name__ == "__main__":
    app.include_router(router=router)
    run(app, host=SERVER_HOST, port=SERVER_PORT)
