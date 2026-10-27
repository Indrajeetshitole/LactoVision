import logging
from typing import Optional

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from .config import get_settings

logger = logging.getLogger(__name__)

_client: Optional[MongoClient] = None


def connect_db() -> None:
    global _client
    settings = get_settings()
    _client = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=5000)
    _client.admin.command("ping")
    logger.info("MongoDB connection established")


def close_db() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None
        logger.info("MongoDB connection closed")


def is_connected() -> bool:
    if _client is None:
        return False
    try:
        _client.admin.command("ping")
        return True
    except PyMongoError:
        return False


def get_database():
    if _client is None:
        raise RuntimeError("MongoDB client is not initialized")
    return _client[get_settings().mongo_db_name]
