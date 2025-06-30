from datetime import datetime

from pydantic import BaseModel, Field

from todo_list_api.models.todos import TodoState


class TodoBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str | None = Field(None, max_length=510)
    state: TodoState = TodoState.draft


class TodoCreate(TodoBase):
    pass


class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime


class TodoResponseList(BaseModel):
    todos: list[TodoResponse]


class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=255)
    description: str | None = Field(default=None, max_length=510)
    state: TodoState | None = None
