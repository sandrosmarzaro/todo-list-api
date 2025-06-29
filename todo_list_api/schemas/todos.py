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


class TodoResponseList(BaseModel):
    todos: list[TodoResponse]
