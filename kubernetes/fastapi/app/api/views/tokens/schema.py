from typing import Annotated, List
from typing_extensions import Doc
from pydantic import BaseModel


class UserDataIn(BaseModel):
    id: Annotated[int, Doc("")]
    email: Annotated[str, Doc("")]
    is_valid: Annotated[bool, Doc("")]
    
class RefreshTokenIn(BaseModel):
    refresh_token: Annotated[ str, Doc("")]


class RefreshTokenOut(BaseModel):
    access_token: Annotated[str, Doc("")]
    token_type: Annotated[str, Doc("")] = "Bearer"
    

class CreateTokenOut(RefreshTokenOut):
    refresh_token: Annotated[ str, Doc("")]
    

class TokenDetailsIn(BaseModel):
    access_token: Annotated[str, Doc("")]
    
class TokenDetails(BaseModel):
    sub: Annotated[str, Doc("")]
    email: Annotated[str, Doc("")]
    superuser: Annotated[bool, Doc("")]
    type: Annotated[str, Doc("")]
    is_verfied: Annotated[bool, Doc("")]
    valid_token: Annotated[bool, Doc("")]
    membership: Annotated[List[dict], Doc("")]
    

class UserTokenMembershipDetails(BaseModel):
    group_id: int
    group_name: str
    membership_id: int
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
