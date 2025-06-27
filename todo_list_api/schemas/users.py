from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=255)


class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    id: int
    username: str = Field(..., min_length=1, max_length=255)
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(UserBase):
    pass


class UserResponseList(BaseModel):
    users: list[UserResponse]
