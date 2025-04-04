from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict

from app.database.postgres.models.groups import Group

from .schema import GroupCreate, GroupOut, GroupUpdate, AddGroupMember, RemoveGroupMember, GetGroupMembers, AddGroupMembers
from ..tokens.schema import TokenDetails, UserTokenMembershipDetails
from ..users.schema import UserOut
from app.database.postgres import crud
from app.database.postgres.models import User
from .helpers import GroupHelper, PermissionHelper, RoleHelper

from .exceptions import Invalid, InsufficientPermissions, GroupException
from ..tokens.services import Token as TokenService
from ..otp.services import OtpService


class UserPermissions:
    def __init__(self) -> None:
        pass
        
    async def membership_token_data(self, token_payload:TokenDetails, group_id: int) -> list:
        for memberships in token_payload.membership:
            if memberships["group_id"] == group_id:
                return UserTokenMembershipDetails(**memberships)
        raise Invalid("User is not a member of the group!", status.HTTP_403_FORBIDDEN)
    
    async def have_permissions(self, membership:UserTokenMembershipDetails, allowed_user_roles:List[str]) -> bool:
        flag = False
        if membership.role in allowed_user_roles:
            flag = True
        return flag
    
    async def can_add_members(self, token_payload:TokenDetails, group_id:int) -> bool:
        membership: UserTokenMembershipDetails = await self.membership_token_data(token_payload, group_id)
        flag = await self.have_permissions(membership, ['admin', 'sub_admin', 'manager'])
        return flag and membership.add_members
    
    async def can_remove_members(self, token_payload:TokenDetails, group_id:int) -> bool:
        membership: UserTokenMembershipDetails = await self.membership_token_data(token_payload, group_id)
        flag = await self.have_permissions(membership, ['admin', 'sub_admin'])
        
        return flag and membership.remove_members
    
    async def can_update_group(self, token_payload:TokenDetails, group_id:int) -> bool:
        membership: UserTokenMembershipDetails = await self.membership_token_data(token_payload, group_id)
        flag = await self.have_permissions(membership, ['admin', 'sub_admin'])
        return flag and membership.edit_group
    
    async def can_delete_group(self, token_payload:TokenDetails, group_id:int) -> bool:
        membership: UserTokenMembershipDetails = await self.membership_token_data(token_payload, group_id)
        flag = await self.have_permissions(membership, ['admin'])
        return flag and membership.edit_group
    
    async def can_view_members(self, token_payload:TokenDetails, group_id:int) -> bool:
        membership: UserTokenMembershipDetails = await self.membership_token_data(token_payload, group_id)
        return True and membership.view_members
    
    async def can_view_group(self, token_payload:TokenDetails, group_id:int) -> bool:
        membership: UserTokenMembershipDetails = await self.membership_token_data(token_payload, group_id)
        return True
    
    async def can_edit_roles(self, token_payload:TokenDetails, group_id:int, target_user_role:str,) -> bool:
        membership = await self.membership_token_data(token_payload, group_id)
        flag = False
        
        if membership.role in ['admin'] and target_user_role in ['admin', 'sub_admin', 'manager', 'member']:
            flag = True
        elif membership.role in ['admin', 'sub_admin'] and target_user_role in ['sub_admin', 'manager', 'member']:
            flag = True
        elif membership.role in ['admin', 'sub_admin', 'manager'] and target_user_role in ['manager', 'member']:
            flag = True
                
        return flag