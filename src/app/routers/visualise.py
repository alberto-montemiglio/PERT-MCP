from typing import Annotated

from fastapi import Depends
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from neo4j import AsyncSession

from app.dependencies import get_async_db_session
from app.services import get_graph

router = APIRouter(prefix="/graphdb/visualise", tags=["Graph DB Visualise"])


@router.get("/")
async def visualise_graph_controller(
    session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> FileResponse:
    """
    Visualise the entire graph database.
    """
    return await get_graph(session)
