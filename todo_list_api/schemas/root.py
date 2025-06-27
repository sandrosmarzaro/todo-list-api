from pydantic import BaseModel


class HealthCheckBase(BaseModel):
    message: str


class HealthCheckResponse(BaseModel):
    message: str
