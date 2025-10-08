
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
    except Exception:
        # if session:
        #     try: 
        #         await session.rollback()
        #     except Exception as rollback_error:
        #         logger.error(f"Failed to rollback session: {rollback_error}")
        #         raise RuntimeError("Failed to rollback session") from rollback_error
        # raise
        logger.error("Session error")
        raise
