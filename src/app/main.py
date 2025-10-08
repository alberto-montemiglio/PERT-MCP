from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import graph_db

app = FastAPI()
app.include_router(graph_db.router)


# Redirect root to docs
@app.get("/")
async def redirect_root() -> RedirectResponse:
    """
    Redirect the root path to the documentation page
    """
    return RedirectResponse(url="/docs")
