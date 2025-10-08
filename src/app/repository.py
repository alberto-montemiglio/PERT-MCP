from typing import Annotated

from fastapi import Depends, Path
from neo4j import AsyncSession

from app.dependencies import get_async_db_session
from app.schemas import Event, Activity


async def create_event(
        session: Annotated[AsyncSession, Depends(get_async_db_session)], 
        event: Annotated[Event, Depends()]
        ) -> Event:
    """
    Create a new event in the database.
    """
    query = """
    CREATE (e:Event {id: $id, name: $name})
    RETURN e
    """
    result = await session.run(query,
                               id=event.id,
                               name=event.name
                               )
    record = await result.single()
    return Event(id=record["e"]["id"], name=record["e"]["name"])


async def list_events(
        session: Annotated[AsyncSession, Depends(get_async_db_session)]
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
        events.append(Event(id=event_node["id"], name=event_node["name"], predecessor_event_id=event_node["predecessor_event_id"]))
    return events


async def get_event(
        session: Annotated[AsyncSession, Depends(get_async_db_session)], 
        event_id: Annotated[str, Path()]
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
        return None
    event_node = record["e"]
    return Event(id=event_node["id"], name=event_node["name"], predecessor_event_id=event_node["predecessor_event_id"], activities_ids=event_node["activities_ids"])

async def delete_event(
        session: Annotated[AsyncSession, Depends(get_async_db_session)], 
        event_id: Annotated[str, Path()]
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
        event: Annotated[Event, Depends()]
        ) -> Event:
    """
    Update an existing event in the database.
    """
    query = """
    MATCH (e:Event {id: $id})
    SET e.name = $name
    RETURN e
    """
    result = await session.run(query,
                               id=event_id,
                               name=event.name
                               )
    record = await result.single()
    if record is None:
        return None
    updated_event_node = record["e"]
    return Event(id=updated_event_node["id"], name=updated_event_node["name"], predecessor_event_id=updated_event_node["predecessor_event_id"], activities_ids=updated_event_node["activities_ids"])

async def create_activity(
        session: Annotated[AsyncSession, Depends(get_async_db_session)], 
        activity: Annotated[Activity, Depends()]
        ) -> Activity:
    """
    Create a new activity in the database.
    """
    query = """
    MATCH (from_event:Event {id: $from_event_id}), (to_event:Event {id: $to_event_id})
    CREATE (from_event)-[r:PRECEDES {id: $id, name: $name, duration: $duration, cost: $cost}]->(to_event)
    RETURN r
    """
    result = await session.run(query,
                               id=activity.id,
                               name=activity.name,
                               from_event_id=activity.from_event_id,
                               to_event_id=activity.to_event_id,
                               duration=activity.duration,
                               cost=activity.cost
                               )
    record = await result.single()
    return Activity(id=record["r"]["id"], name=record["r"]["name"], from_event_id=record["r"]["from_event_id"], to_event_id=record["r"]["to_event_id"], duration=record["r"]["duration"], cost=record["r"]["cost"])

async def list_activities(
        session: Annotated[AsyncSession, Depends(get_async_db_session)]
        ) -> list[Activity]:
    """
    List all activities in the database.
    """
    query = """
    MATCH ()-[r:PRECEDES]->()
    RETURN r
    """
    result = await session.run(query)
    activities = []
    async for record in result:
        activity_rel = record["r"]
        activities.append(Activity(id=activity_rel["id"], name=activity_rel["name"], from_event_id=activity_rel.start_node["id"], to_event_id=activity_rel.end_node["id"], duration=activity_rel["duration"], cost=activity_rel["cost"]))
    return activities

async def get_activity(
        session: Annotated[AsyncSession, Depends(get_async_db_session)], 
        activity_id: Annotated[str, Path()]
        ) -> Activity:
    """
    Get an activity by its ID from the database.
    """
    query = """
    MATCH ()-[r:PRECEDES]->()
    WHERE r.id = $id
    RETURN r
    """
    result = await session.run(query, id=activity_id)
    record = await result.single()
    if record is None:
        return None
    activity_rel = record["r"]
    return Activity(id=activity_rel["id"], name=activity_rel["name"], from_event_id=activity_rel.start_node["id"], to_event_id=activity_rel.end_node["id"], duration=activity_rel["duration"], cost=activity_rel["cost"])
async def delete_activity(
        session: Annotated[AsyncSession, Depends(get_async_db_session)], 
        activity_id: Annotated[str, Path()]
        ) -> None:
    """
    Delete an activity by its ID from the database.
    """
    query = """
    MATCH ()-[r:PRECEDES]->()
    WHERE r.id = $id
    DELETE r
    """
    await session.run(query, id=activity_id)
    return None

async def update_activity(
        session: Annotated[AsyncSession, Depends(get_async_db_session)], 
        activity_id: Annotated[str, Path()],
        activity: Annotated[Activity, Depends()]
        ) -> Activity:
    """
    Update an existing activity in the database.
    """
    query = """
    MATCH ()-[r:PRECEDES]->()
    WHERE r.id = $id
    SET r.name = $name, r.from_event_id = $from_event_id, r.to_event_id = $to_event_id, r.duration = $duration, r.cost = $cost
    RETURN r
    """
    result = await session.run(query,
                               id=activity_id,
                               name=activity.name,
                               from_event_id=activity.from_event_id,
                               to_event_id=activity.to_event_id,
                               duration=activity.duration,
                               cost=activity.cost
                               )
    record = await result.single()
    if record is None:
        return None
    updated_activity_rel = record["r"]
    return Activity(id=updated_activity_rel["id"], name=updated_activity_rel["name"], from_event_id=updated_activity_rel.start_node["id"], to_event_id=updated_activity_rel.end_node["id"], duration=updated_activity_rel["duration"], cost=updated_activity_rel["cost"])
