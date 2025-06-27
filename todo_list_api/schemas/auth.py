from pydantic import BaseModel


class TokenBase(BaseModel):
    token_type: str
    access_token: str


class TokenResponse(TokenBase):
    pass
