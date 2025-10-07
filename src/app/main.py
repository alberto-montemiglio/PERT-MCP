from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


# Redirect root to docs
@app.get("/")
async def redirect_root() -> RedirectResponse:
    """
    Redirect the root path to the documentation page
    """
    return RedirectResponse(url="/docs")