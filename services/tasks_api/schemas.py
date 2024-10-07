from uuid import UUID

from pydantic import BaseModel, ConfigDict

from models import TaskStatus


class CreateTask(BaseModel):
    title: str


class APITask(BaseModel):
    id: UUID
    title: str
    status: TaskStatus
    owner: str

    model_config = ConfigDict(from_attributes=True)


class APITaskList(BaseModel):
    results: list[APITask]

    model_config = ConfigDict(from_attributes=True)


class CloseTask(BaseModel):
    id: UUID
