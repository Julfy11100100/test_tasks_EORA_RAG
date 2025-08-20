from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.api import questions
from app.containers import Container
from app.utils.logging import logger
from config import settings


def init_dependency_injector() -> Container:
    """Инициализация инъекций"""
    container = Container()
    container.config.from_pydantic(settings=settings, required=True)
    container.wire(
        modules=[questions]
    )
    return container


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Startup")
    init_dependency_injector()
    yield
    logger.info("Shutdown")


# Создание FastAPI приложения
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
    swagger_ui_parameters={
        "docExpansion": "none",
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True
    }
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Отловили ошибку: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Произошла внутренняя ошибка. Мы уже работаем над её устранением."}
    )


# Подключение роутов
app.include_router(questions.router, prefix="/api/v1", tags=["questions"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
