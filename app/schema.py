import re
from pydantic import BaseModel, validator
from typing import Optional


class User(BaseModel):
    id: str
    full_name: str
    email_address: Optional[str]

    class Config:
        orm_mode = True

    @validator('email_address')
    def valid_email_address(cls, v):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, v):
            raise ValueError('not a valid email address')
        return v

    @validator('full_name')
    def valid_full_name(cls, v):
        return v.title()
