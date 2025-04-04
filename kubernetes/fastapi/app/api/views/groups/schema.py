from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr, Field

from app.api.views.users.schema import UserOut



class GroupCreate(BaseModel):
    name: str
    description: str

class GroupUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

class GetGroupMembers(BaseModel):
    members: Optional[List[UserOut]]

class AddGroupMember(BaseModel):
    group_id: int
    email: EmailStr

class RemoveGroupMember(BaseModel):
    user_id: int
    
class AddGroupMembers(BaseModel):
    emails: List[EmailStr]

class RemoveGroupMembers(BaseModel):
    user_ids: List[int]
    

class GroupUserMembershipOut(BaseModel):
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

class GroupUserOut(BaseModel):
    full_name: str
    email: EmailStr
    membership: List[GroupUserMembershipOut]

class GroupOut(BaseModel):
    id: int
    name: str
    description: str
    members: Optional[List[GroupUserOut]]
    created_at: datetime
    updated_at: Optional[datetime]
    

class CreateRole(BaseModel):
    name: str

class CreatePermission(BaseModel):
    role_id: int
    member: Dict[str, bool]
    subscription: Dict[str, bool]