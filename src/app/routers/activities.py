from typing import Annotated
from fastapi.routing import APIRouter
from fastapi import Depends
from app.repository import create_activity, list_activities, get_activity, delete_activity, update_activity

from app.schemas import Activity


router = APIRouter(prefix="/graphdb/activities", tags=["graphdb_activities"])


@router.post("/create/")
async def create_activity(
        activity: Annotated[Activity, Depends()],
    ) -> Activity:
    """
    Create a new activity in the database.
    """
    return activity

@router.get("/list/")
async def list_activities(
        activities = Annotated[list[Activity], Depends(list_activities)],
        ) -> list[Activity]:
    """
    List all activities in the database.
    """
    return activities

@router.get("/get/{activity_id}")
async def get_activity(
        activity = Annotated[Activity, Depends(get_activity)],
        ) -> Activity:
    """
    Get an activity by its ID from the database.
    """
    return activity

@router.delete("/delete/{activity_id}")
async def delete_activity(
        result = Annotated[None, Depends(delete_activity)],
        ) -> None:
    """
    Delete an activity by its ID from the database.
    """
    return result

@router.put("/update/{activity_id}")
async def update_activity(
        activity = Annotated[Activity, Depends(update_activity)],
        ) -> Activity:
    """
    Update an existing activity in the database.
    """
    return activity
