from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError

from migrations import run_migrations
from service.api.authorization.endpoints import auth_router
from settings import DEFAULT_DATABASE

app = FastAPI()

app.include_router(auth_router, prefix="/api/authorization")


@app.on_event("startup")
async def startup_event():
    run_migrations(DEFAULT_DATABASE)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return Response(status_code=400, content=str(exc))
