from fastapi import APIRouter

from ..database import is_connected

router = APIRouter(tags=["Health"])


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "LactoVision API",
    }


@router.get("/database/health")
def database_health():
    connected = is_connected()
    return {
        "status": "ok" if connected else "error",
        "service": "MongoDB",
        "connected": connected,
    }
