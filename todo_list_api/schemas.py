from pydantic import BaseModel


class MessageClass(BaseModel):
    message: str
