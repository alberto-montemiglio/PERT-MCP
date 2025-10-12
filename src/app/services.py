import asyncio
import tempfile
from typing import Annotated

import matplotlib.pyplot as plt
import networkx as nx
from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from loguru import logger
from neo4j import AsyncSession

from app.dependencies import get_async_db_session
from app.schemas import Activity, Event


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


async def get_graph(
    session=Annotated[AsyncSession, Depends(get_async_db_session)],
) -> FileResponse:
    G = nx.Graph()
    query = """
    MATCH (n)-[r]->(m)
    RETURN n, r, m
    """
    result = await session.run(query)
    data = await result.data()

    for nrm in data:
        n, r, m = nrm["n"], nrm["r"], nrm["m"]
        n_event = Event(id=str(n["id"]), name=n["name"])
        m_event = Event(id=str(m["id"]), name=m["name"])
        r_activity = Activity(
            id=r[0]["id"],
            name=r[0].get("name", ""),
            duration=r[0].get("duration", 0),
            cost=r[0].get("cost", 0),
            from_event_id=r[0]["from_event_id"],
            to_event_id=r[0]["to_event_id"],
        )

        G.add_node(n_event.id, **n_event.dict())
        G.add_node(m_event.id, **m_event.dict())
        G.add_edge(n_event.id, m_event.id, **r_activity.dict())

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    node_labels = {
        node: "ID: " + data.get("id", "") + "\nName: " + data.get("name", "")
        for node, data in G.nodes(data=True)
    }
    nx.draw_networkx(
        G,
        pos,
        with_labels=True,
        labels=node_labels,
        node_color="lightblue",
        node_size=2000,
        font_size=10,
        font_weight="bold",
        arrows=True,
    )

    edge_labels = {
        (u, v): "Name: "
        + d.get("name", "")
        + "\nFrom Event "
        + d.get("from_event_id", "")
        + "\nTo Event "
        + d.get("to_event_id", "")
        + "\nDuration: "
        + str(d.get("duration", 0))
        + "\nCost: "
        + str(d.get("cost", 0))
        for u, v, d in G.edges(data=True)
    }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        plt.savefig(tmp_file.name, format="png")
        plt.close()

        return FileResponse(tmp_file.name, media_type="image/png", filename="graph.png")
