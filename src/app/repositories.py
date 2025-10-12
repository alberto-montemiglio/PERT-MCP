from typing import Annotated

from fastapi import Depends, Path
from loguru import logger
from neo4j import AsyncSession

from app.dependencies import get_async_db_session
from app.schemas import Activity, Event


async def create_event(
    session: Annotated[AsyncSession, Depends(get_async_db_session)],
    event: Annotated[Event, Depends()],
) -> Event:
    """
    Create a new event in the database.
    """
    query = """
    CREATE (e:Event {id: $id, name: $name})
    RETURN e
    """
    try:
        result = await session.run(query, id=event.id, name=event.name)
        record = await result.single()
        if record is None:
            logger.error("Failed to create event: No record returned")
            raise RuntimeError("Failed to create event: No record returned")
        return Event(id=record["e"]["id"], name=record["e"]["name"])
    except Exception as e:
        logger.error(f"Error creating event: {e}")
        raise RuntimeError(f"Failed to create event: {e}") from e


async def list_events(
    session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> list[Event]:
    """
    List all events in the database.
    """
    query = """
    MATCH (e:Event)
    RETURN e
    """
    result = await session.run(query)
    events = []
    async for record in result:
        event_node = record["e"]
        events.append(
            Event(
                id=event_node["id"],
                name=event_node["name"],
            )
        )
    return events


async def get_event(
    session: Annotated[AsyncSession, Depends(get_async_db_session)],
    event_id: Annotated[str, Path()],
) -> Event:
    """
    Retrieve an event by its ID from the database.
    """
    query = """
    MATCH (e:Event {id: $id})
    RETURN e
    """
    result = await session.run(query, id=event_id)
    record = await result.single()
    if record is None:
        logger.error(f"Event with ID {event_id} not found")
        raise RuntimeError(f"Event with ID {event_id} not found")
    event_node = record["e"]
    return Event(
        id=event_node["id"],
        name=event_node["name"],
    )


async def delete_event(
    session: Annotated[AsyncSession, Depends(get_async_db_session)],
    event_id: Annotated[str, Path()],
) -> None:
    """
    Delete an event by its ID from the database.
    """
    query = """
    MATCH (e:Event {id: $id})
    DETACH DELETE e
    """
    await session.run(query, id=event_id)
    return None


async def update_event(
    session: Annotated[AsyncSession, Depends(get_async_db_session)],
    event_id: Annotated[str, Path()],
    event: Annotated[Event, Depends()],
) -> Event:
    """
    Update an existing event in the database.
    """
    query = """
    MATCH (e:Event {id: $id})
    SET e.name = $name
    RETURN e
    """
    result = await session.run(query, id=event_id, name=event.name)
    record = await result.single()
    if record is None:
        logger.error(f"Event with ID {event_id} not found")
        raise RuntimeError(f"Event with ID {event_id} not found")
    updated_event_node = record["e"]
    return Event(
        id=updated_event_node["id"],
        name=updated_event_node["name"],
    )


async def create_activity(
    session: Annotated[AsyncSession, Depends(get_async_db_session)],
    activity: Annotated[Activity, Depends()],
) -> Activity:
    """
    Create a new activity in the database.
    """
    # First, check if an activity with this ID already exists
    check_query = """
    MATCH ()-[r:Activity {id: $id}]->()
    RETURN r LIMIT 1
    """
    check_result = await session.run(check_query, id=activity.id)
    existing_record = await check_result.single()

    if existing_record is not None:
        logger.error(f"Activity with ID {activity.id} already exists")
        raise ValueError(f"Activity with ID '{activity.id}' already exists")

    # Proceed with creation if ID is unique
    query = """
    MATCH (from_event:Event {id: $from_event_id}), (to_event:Event {id: $to_event_id})
    CREATE (from_event)-[r:Activity {
        id: $id,
        name: $name,
        duration: $duration,
        cost: $cost,
        from_event_id: $from_event_id,
        to_event_id: $to_event_id
    }]->(to_event)
    RETURN r
    """
    try:
        result = await session.run(
            query,
            id=activity.id,
            name=activity.name,
            from_event_id=activity.from_event_id,
            to_event_id=activity.to_event_id,
            duration=activity.duration,
            cost=activity.cost,
        )
        record = await result.single()
        if record is None:
            logger.error("Failed to create activity: No record returned")
            raise RuntimeError("Failed to create activity: No record returned")
        return Activity(
            id=record["r"]["id"],
            name=record["r"]["name"],
            from_event_id=record["r"]["from_event_id"],
            to_event_id=record["r"]["to_event_id"],
            duration=record["r"]["duration"],
            cost=record["r"]["cost"],
        )
    except Exception as e:
        logger.error(f"Error creating activity: {e}")
        raise RuntimeError(f"Failed to create activity: {e}") from e


async def get_activity(
    session: Annotated[AsyncSession, Depends(get_async_db_session)],
    activity_id: Annotated[str, Path()],
) -> Activity:
    """
    Get an activity by its ID from the database.
    """
    query = """
    MATCH ()-[r:Activity]->()
    WHERE r.id = $id
    RETURN r
    """
    result = await session.run(query, id=activity_id)
    record = await result.single()
    if record is None:
        logger.error(f"Activity with ID {activity_id} not found")
        raise RuntimeError(f"Activity with ID {activity_id} not found")
    activity_rel = record["r"]
    return Activity(
        id=activity_rel["id"],
        name=activity_rel["name"],
        from_event_id=activity_rel.start_node["id"],
        to_event_id=activity_rel.end_node["id"],
        duration=activity_rel["duration"],
        cost=activity_rel["cost"],
    )


async def delete_activity(
    session: Annotated[AsyncSession, Depends(get_async_db_session)],
    activity_id: Annotated[str, Path()],
) -> None:
    """
    Delete an activity by its ID from the database.
    """
    query = """
    MATCH ()-[r:Activity]->()
    WHERE r.id = $id
    DELETE r
    """
    await session.run(query, id=activity_id)
    return None


async def update_activity(
    session: Annotated[AsyncSession, Depends(get_async_db_session)],
    activity_id: Annotated[str, Path()],
    activity: Annotated[Activity, Depends()],
) -> Activity:
    """
    Update an existing activity in the database.
    """
    query = """
    MATCH ()-[r:Activity]->()
    WHERE r.id = $id
    SET r.name = $name, r.from_event_id = $from_event_id, r.to_event_id = $to_event_id, r.duration = $duration, r.cost = $cost
    RETURN r
    """
    result = await session.run(
        query,
        id=activity_id,
        name=activity.name,
        from_event_id=activity.from_event_id,
        to_event_id=activity.to_event_id,
        duration=activity.duration,
        cost=activity.cost,
    )
    record = await result.single()
    if record is None:
        logger.error("Failed to update activity: No record returned")
        raise RuntimeError("Failed to update activity: No record returned")
    updated_activity_rel = record["r"]
    return Activity(
        id=updated_activity_rel["id"],
        name=updated_activity_rel["name"],
        from_event_id=updated_activity_rel.start_node["id"],
        to_event_id=updated_activity_rel.end_node["id"],
        duration=updated_activity_rel["duration"],
        cost=updated_activity_rel["cost"],
    )
