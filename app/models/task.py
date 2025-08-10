from pydantic import BaseModel
from typing import Optional


class TaskBase(BaseModel):
    title: str
    location: Optional[str] = None
    schedule: Optional[str] = None
    mood: Optional[str] = None  # humor


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    schedule: Optional[str] = None
    mood: Optional[str] = None


class TaskRead(TaskBase):
    id: int

    model_config = {
        "from_attributes": True,
    }
