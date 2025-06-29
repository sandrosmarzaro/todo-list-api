from pydantic import BaseModel, Field

from todo_list_api.models.todos import TodoState


class FilterPage(BaseModel):
    limit: int = Field(ge=0, default=10)
    offset: int = Field(ge=0, default=0)


class FilterTodo(FilterPage):
    title: str | None = Field(default=None, min_length=3, max_length=255)
    description: str | None = Field(default=None, min_length=3, max_length=510)
    state: TodoState | None = None
