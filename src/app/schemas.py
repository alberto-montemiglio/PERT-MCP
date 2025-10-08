from pydantic import BaseModel


class Activity(BaseModel):
    id: str
    name: str
    from_event_id: str
    to_event_id: str
    duration: int
    cost: float | None = None


class Event(BaseModel):
    id: str
    name: str
