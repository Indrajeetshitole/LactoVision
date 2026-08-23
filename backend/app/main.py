import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import get_settings
from .database import close_db, connect_db
from .routes.health import router as health_router
from .routes.system import router as system_router
from .routes.auth import router as auth_router
from .routes.farms import router as farms_router
from .routes.cows import router as cows_router
from .routes.milk import router as milk_router
from .routes.feed import router as feed_router
from .routes.health_records import router as health_records_router
from .routes.environment import router as environment_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("lactovision")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        connect_db()
    except Exception as exc:
        # Backend remains available so /api/health can still be tested.
        # Database endpoints will report the connection failure.
        logger.exception("MongoDB startup connection failed: %s", exc)
    yield
    close_db()


settings = get_settings()

app = FastAPI(
    title="LactoVision API",
    version="1.0.0",
    description="Phase 1 foundation for LactoVision – A Milk Yield Optimization AI",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(system_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(farms_router, prefix="/api")
app.include_router(cows_router, prefix="/api")
app.include_router(milk_router, prefix="/api")
app.include_router(feed_router, prefix="/api")
app.include_router(health_records_router, prefix="/api")
app.include_router(environment_router, prefix="/api")


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
