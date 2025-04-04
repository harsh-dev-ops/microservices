from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr, Field


class UserRegisteration(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    confirm_password: Optional[str] = None

class UpdatePassword(BaseModel):
    password: str
    confirm_password: str

class UserRegisterationOut(BaseModel):
    message: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

class Permissions(BaseModel):
    member: Dict[str, bool]
    subscription: Dict[str, bool]


class Roles(BaseModel):
    name: str
    permissions: Permissions


class UserOut(BaseModel):
    email: str
    full_name: str
    phone: Optional[str]
    is_verified: bool
    is_email_verified: bool
    is_phone_verified: bool
    superuser: bool
    created_at: datetime
    updated_at: Optional[datetime]

class GroupOut(BaseModel):
    id: int
    name: str


class UserMembershipOut(BaseModel):
    group: GroupOut
    id: int
    role: str
    add_members: bool
    view_members: bool
    remove_members: bool
    edit_members: bool
    edit_roles: bool
    buy_subscription: bool
    edit_subscription: bool
    view_subscription: bool
    edit_group: bool
    
    
class UserDetailsOut(UserOut):
    membership: Optional[List[UserMembershipOut]] = None

