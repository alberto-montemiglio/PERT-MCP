import asyncio

from fastapi import FastAPI
from loguru import logger


async def wait_for_db_connection(app: FastAPI):
    """
    Wait for the database connection to be established.
    """
    logger.debug("Waiting for the database connection to be established...")
    for i in range(20):
        try:
            await asyncio.sleep(2)
            async with app.state.driver.session() as session:
                await session.run("RETURN 1")
            logger.info("Database connection established")
            return
        except Exception as e:
            logger.warning(f"Database connection failed, retrying... ({i + 1}/20)")
            if i == 19:
                logger.error("Failed to connect to the database after 20 attempts")
                raise RuntimeError("Failed to connect to the database") from e


async def create_event_uniqueness_constraints(app: FastAPI):
    """
    Create uniqueness constraints for Event and Activity IDs.
    """
    try:
        async with app.state.driver.session() as session:
            await session.run("""
            CREATE CONSTRAINT event_id_unique IF NOT EXISTS
            FOR (e:Event)
            REQUIRE e.id IS UNIQUE;
            """)
    except Exception as e:
        logger.error(f"Error creating uniqueness constraints: {e}")
        raise RuntimeError("Failed to create uniqueness constraints") from e