from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter

from app.repositories import (
    create_activity,
    delete_activity,
    get_activity,
    update_activity,
)
from app.schemas import Activity

router = APIRouter(prefix="/graphdb/activities", tags=["graphdb_activities"])


@router.post("/create/")
async def create_activity_controller(
    activity: Annotated[Activity, Depends(create_activity)],
) -> Activity:
    """
    Create a new activity in the database.
    """
    return activity


@router.get("/get/{activity_id}")
async def get_activity_controller(
    activity: Annotated[Activity, Depends(get_activity)],
) -> Activity:
    """
    Get an activity by its ID from the database.
    """
    return activity


@router.delete("/delete/{activity_id}")
async def delete_activity_controller(
    result: Annotated[None, Depends(delete_activity)],
) -> None:
    """
    Delete an activity by its ID from the database.
    """
    return result


@router.put("/update/{activity_id}")
async def update_activity_controller(
    activity: Annotated[Activity, Depends(update_activity)],
) -> Activity:
    """
    Update an existing activity in the database.
    """
    return activity
