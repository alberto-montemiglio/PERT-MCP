from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter

from app.repositories import (
    create_event,
    delete_event,
    get_event,
    list_events,
)
from app.schemas import Event

router = APIRouter(prefix="/graphdb/events", tags=["Graph DB Events"])


@router.post("/create/")
async def create_event_controller(
    event: Annotated[Event, Depends(create_event)],
) -> Event:
    return event


@router.get("/list/")
async def list_events_controller(
    events: Annotated[list[Event], Depends(list_events)],
) -> list[Event]:
    return events


@router.get("/get/{event_id}")
async def get_event_controller(
    event: Annotated[Event, Depends(get_event)],
) -> Event:
    return event


@router.delete("/delete/{event_id}")
async def delete_event_controller(
    result: Annotated[None, Depends(delete_event)],
) -> None:
    return result
