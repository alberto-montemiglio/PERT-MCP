from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter

from app.visualise import visualise_graph


router = APIRouter(prefix="/graphdb/visualise", tags=["Graph DB Visualise"])

@router.get("/")
async def visualise_graph_controller(
    graph_image = Annotated[bytes, Depends(visualise_graph)],
    ) -> bytes:
    """
    Visualise the entire graph database.
    """
    return graph_image