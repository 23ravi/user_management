from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class User(BaseModel):
    firstname: str
    lastname: str
    dob: str
    address: str
    gender: str
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=15)
    
    @field_validator('dob')
    def validate_dob_format(cls, v):
        # Regular expression to match the date format YYYY-MM-DD
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(date_pattern, v):
            raise ValueError('dob must be in YYYY-MM-DD format')
        return v
    
    class Config:
        # Ensure that input data for dob is correctly formatted
        # e.g., automatically parse string dates into ISO format
        anystr_strip_whitespace = True