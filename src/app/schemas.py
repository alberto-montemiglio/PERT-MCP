from pydantic import BaseModel


class Event(BaseModel):
    id: str
    predecessors_ids: list[str]
    name: str
    successors_ids: list[str]
