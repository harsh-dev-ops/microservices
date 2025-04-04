from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class OtpSend(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    
class OtpIn(BaseModel):
    otp: str = Field(str, min_length=4, max_length=6)
    
class OtpDBIn(BaseModel):
    email_or_phone: str
    user_id: int
    otp: str