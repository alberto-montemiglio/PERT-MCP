from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.driver = AsyncGraphDatabase.driver(
        uri=get_env_variable("NEO4J_DB_URI"),
        auth=Auth("basic", get_env_variable("NEO4J_DB_USER"), get_env_variable("NEO4J_DB_PASSWORD"))
    )
    yield
    await app.state.driver.close()


app = FastAPI(lifespan=lifespan)
app.include_router(events.router)
app.include_router(activities.router)

# Redirect root to docs
@app.get("/")
async def redirect_root() -> RedirectResponse:
    """
    Redirect the root path to the documentation page
    """
    return RedirectResponse(url="/docs")