from neo4j_viz.neo4j import from_neo4j
from typing import Annotated
from fastapi import Depends
from neo4j import AsyncSession
from app.dependencies import get_async_db_session


def get_graph(
    session = Annotated[AsyncSession, Depends(get_async_db_session)],
    ):
    query = """
    MATCH (n)-[r]->(m)
    RETURN n, r, m
    """
    result = await session.run(query)
    return result

async def visualise_graph(
    result = Annotated[AsyncSession, Depends(get_graph)],
    ) -> bytes:
    """
    Visualise the entire graph database.
    """
    # Convert the Neo4j result to a graph visualization (VG)
    VG = from_neo4j(result)
    # Render the graph visualization to an image (PNG format)
    png_image = VG.render("png")