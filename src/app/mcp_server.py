from fastmcp import FastMCP
from contextlib import asynccontextmanager
from fastapi import FastAPI
from main import app, lifespan as app_lifespan

# Generate the MCP server from the FastAPI app
mcp = FastMCP.from_fastapi(app=app, name="PERT-MCP")

# Create the MCP's ASGI app
mcp_app = mcp.http_app(path='/mcp')


# Combine both lifespans
@asynccontextmanager
async def combined_lifespan(app: FastAPI):
    async with app_lifespan(app):
        async with mcp_app.lifespan(app):
            yield

# Create a new FastAPI app that combines both sets of routes
combined_app = FastAPI(
    title="PERT-MCP Combined API",
    routes=[
        *mcp_app.routes,
        *app.routes,
    ],
    lifespan=combined_lifespan,
)

if __name__ == "__main__":
    combined_app.run()