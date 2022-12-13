import re
from pydantic import BaseModel, validator
from typing import Optional


class UserBase(BaseModel):
    email: str
    full_name: str
    id: str | None = None
    age: int | None = None

    @validator('email')
    def valid_email_address(cls, v):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, v):
            raise ValueError('not a valid email address')
        return v

    @validator('full_name')
    def valid_full_name(cls, v):
        return v.title()

    @validator('age')
    def valid_age(cls, v):
        if v is not None and not 0 < v < 120:
            raise ValueError('Are you sure you are a human??')
        return v


class UserUpdate(UserBase):
    email: Optional[str] = None
    full_name: Optional[str] = None

    class Config:
        orm_mode = True


