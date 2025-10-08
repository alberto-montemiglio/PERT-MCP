from typing import AsyncGenerator

from fastapi import Request
from loguru import logger
from neo4j import AsyncSession


async def get_async_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Get an asynchronous database session.
    """
    driver = request.app.state.driver
    if driver is None:
        raise RuntimeError("Database driver is not initialized")

    session = None
    try:
        session = driver.session()
        async with session:
            yield session
    except Exception as e:
        logger.error(f"Error getting database session: {e}")
        raise RuntimeError("Failed to get database session") from e
