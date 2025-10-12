from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from neo4j import AsyncGraphDatabase, Auth

from app.routers import activities, events, visualise
from app.services import create_event_uniqueness_constraints, wait_for_db_connection
from utils import get_env_variable

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize and close the database driver and create uniqueness constraints for Events and Activities IDs.
    """
    app.state.driver = AsyncGraphDatabase.driver(
        uri=get_env_variable("NEO4J_DB_URI"),
        auth=Auth(
            "basic",
            get_env_variable("NEO4J_DB_USER"),
            get_env_variable("NEO4J_DB_PASSWORD"),
        ),
    )
    await wait_for_db_connection(app)
    await create_event_uniqueness_constraints(app)
    yield
    await app.state.driver.close()


app = FastAPI(lifespan=lifespan)
app.include_router(events.router)
app.include_router(activities.router)
app.include_router(visualise.router)


# Redirect root to docs
@app.get("/")
async def redirect_root() -> RedirectResponse:
    """
    Redirect the root path to the documentation page
    """
    return RedirectResponse(url="/docs")
