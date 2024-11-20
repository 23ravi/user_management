from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

class User(BaseModel):
    firstname: str
    lastname: str
    dob: date
    address: str
    gender: str
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=15)