from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict

from .schema import GroupCreate, GroupOut, GroupUpdate, AddGroupMember, RemoveGroupMember, GetGroupMembers, AddGroupMembers
from .permissions import UserPermissions
from ..tokens.schema import TokenDetails
from ..users.schema import UserOut
from app.database.postgres import crud
from app.database.postgres.models import User, Group
from .helpers import GroupHelper, PermissionHelper, RoleHelper

from .exceptions import Invalid, InsufficientPermissions, GroupException
from ..tokens.services import Token as TokenService
from ..otp.services import OtpService


    

class MembershipService:

    def __init__(self) -> None:
        self._crud = crud.get('user_groups')
        self._permission_helper = PermissionHelper()
    
    async def create(self, db:Session, role:str, user_id:int, group_id:int,):
        data = {
            "role": role,
            "user_id": user_id,
            "group_id": group_id,
        }
        
        permissions= await self._permission_helper.get_permissions(role)
        for permission in permissions:
            data[permission] = True
            
        role_obj = await self._crud.create(db, data)
        return role_obj
    
    
class GroupService:

    def __init__(self) -> None:
        self._group_crud = crud.get('group_crud')
        self._user_crud = crud.get('user_crud')
        self._mebership_service = MembershipService()
        self._user_permissions = UserPermissions()
    
    async def details(self, db:Session, group_id:int, token_payload:TokenDetails) -> GroupOut:
        
        group_obj = await self._group_crud.get(db, group_id)
        return group_obj
    
    async def create(self, db:Session, data: GroupCreate, token_payload:TokenDetails, background_tasks:BackgroundTasks):
        
        if await self._group_crud.get_by_name(db, data.name):
            raise GroupException(f"Group Already Exists with: {data.name}!" )
        
        user_obj: User = await self._user_crud.get(db, int(token_payload.sub))
        
        if not len(user_obj.groups) < 3:
            raise GroupException("Group limit exceeded!")
        
        group_obj: Group = await self._group_crud.create(db, data.model_dump())

        membership_obj = await self._mebership_service.create(db, 'admin', user_obj.id, group_obj.id)
        
        return group_obj
    
    async def update(self, db:Session, token_payload:TokenDetails, group_id:int, data:GroupUpdate):
        
        flag = await self._user_permissions.can_update_group(token_payload, group_id)
        if not flag:
            raise InsufficientPermissions("User has insufficient permission. Please Upgrade your role.")
        
        data = data.model_dump(exclude_none=True)
        return await self._group_crud.update(db, group_id, data)
    
    async def delete(self, db:Session, token_payload:TokenDetails, group_id:int):
        
        flag = await self._user_permissions.can_delete_group(token_payload, group_id)
        if not flag:
            raise InsufficientPermissions("User has insufficient permission. Please Upgrade your role.")

        return await self._group_crud.delete(db, group_id)
    
    async def add_member(self, db:Session, token_payload:TokenDetails, background_tasks:BackgroundTasks, group_id:int, data:AddGroupMember):
        
        flag = await self._user_permissions.can_add_members(token_payload, group_id)
        if not flag:
            raise InsufficientPermissions("User has insufficient permission. Please Upgrade your role.")
        
        group_obj: Group = await self._group_crud.get(db, group_id)
        
        user_obj: User =  await self._user_crud.get_by_email(db, data.email)
        
        if not user_obj:
            user_obj = await self._user_crud.create(db, {"email": data.email})
        
        membership_obj = await self._mebership_service.create(db, 'member', user_obj.id, group_obj.id)
        
        # TODO: send an email of invitation
        
        return user_obj
    
    async def remove_member(self, db:Session, token_payload:TokenDetails, background_tasks:BackgroundTasks, group_id:int, user_id:int):
        
        flag = await self._user_permissions.can_remove_members(token_payload, group_id)
        if not flag:
            raise InsufficientPermissions("User has insufficient permission. Please Upgrade your role.")
        
        group_obj: Group = await self._group_crud.get(db, group_id)
        
        target_member = None
        async for member in group_obj.members:
            if member.user_id == user_id:
                target_member: User = member
                
        if not target_member:
            raise Invalid("User is not a member of the group!", status.HTTP_403_FORBIDDEN)

    
    async def get_member(self, db:Session,  token_payload:TokenDetails, group_id:int, user_id:int) -> UserOut:
        flag = await self._user_permissions.can_view_members(token_payload, group_id)
        if not flag:
            raise InsufficientPermissions("User has insufficient permission. Please Upgrade your role.")
        
        group_obj: Group = await self._group_crud.get(db, group_id)

        target_member = None
        async for member in group_obj.members:
            if member.user_id == user_id:
                target_member: User = member
                
        if not target_member:
            raise Invalid("User is not a member of the group!", status.HTTP_403_FORBIDDEN)
        
        return target_member
    
    async def get_members(self, db:Session, token_payload:TokenDetails, background_tasks:BackgroundTasks, group_id: int):
        flag = await self._user_permissions.can_view_members(token_payload, group_id)
        if not flag:
            raise InsufficientPermissions("User has insufficient permission. Please Upgrade your role.")
        
        group_obj: Group = await self._group_crud.get(db, group_id)
        
        return group_obj
        
    async def get_user_permissions(self, token_payload:TokenDetails, group_id:int):
        return await self._user_permissions.membership_token_data(token_payload, group_id)
    
    # Multiple members
    async def add_members(self, db:Session, data:AddGroupMembers, token_payload:TokenDetails, background_tasks:BackgroundTasks):
        pass
    
    async def remove_members(self, db:Session, data:AddGroupMembers, token_payload:TokenDetails, background_tasks:BackgroundTasks):
        pass
    
