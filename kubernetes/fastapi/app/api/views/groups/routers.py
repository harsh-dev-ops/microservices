from typing import Annotated
from fastapi import APIRouter, Query, Request, Response, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse

from app.database.postgres.deps import db_dependency
from . import services, schema
from app.api.auth.deps import token_details, get_token

router = APIRouter(include_in_schema=False, deprecated=True)

group_service = services.GroupService()

@router.get('/info/{_id}', response_model=schema.GroupOut)
async def get_group_info(
    request: Request, 
    response: Response, 
    token_payload: token_details,
    db: db_dependency, 
    _id: int
    ):
    return await group_service.details(db, _id, token_payload)


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schema.GroupOut)
async def register_group(
    request: Request, 
    response: Response,
    token_payload: token_details, 
    data: schema.GroupCreate, 
    db: db_dependency, 
    background_tasks: BackgroundTasks
    ):
    return await group_service.create(db, data, token_payload, background_tasks)


@router.patch('/update{group_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_group(
    request: Request, 
    response: Response,
    token_payload: token_details, 
    group_id: int,
    data: schema.GroupUpdate, 
    db: db_dependency,
):
    return await group_service.update(db, token_payload, group_id, data)


@router.delete('/delete/{group_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    request: Request, 
    response: Response,
    token_payload: token_details, 
    db: db_dependency, 
    group_id:int,
):
    return await group_service.delete(db, token_payload, group_id)


@router.get('/members/{group_id}', response_model=schema.GetGroupMembers)
async def get_group_members(
    request: Request, 
    response: Response, 
    token_payload: token_details,
    db: db_dependency, 
    group_id: int,
    ):
    return await group_service.get_members(db, token_payload, group_id)


@router.get('/member/{group_id}/{user_id}')
async def get_group_member(
    request: Request, 
    response: Response, 
    token_payload: token_details,
    db: db_dependency, 
    background_tasks: BackgroundTasks,
    group_id: int,
    user_id: int
    ):
    return await group_service.get_member(db, token_payload, group_id, user_id)


@router.get('/user-permissions/{group_id}')
async def get_user_permissions(
    request: Request, 
    response: Response, 
    token_payload: token_details,
    group_id: int,
    ):
    return await group_service.get_user_permissions(token_payload, group_id)


@router.post('/add-member/{group_id}', status_code=status.HTTP_201_CREATED)
async def add_group_member(
    request: Request, 
    response: Response,
    token_payload: token_details,  
    db: db_dependency, 
    background_tasks: BackgroundTasks,
    group_id:int,
    data: schema.AddGroupMember,
    ):
    return await group_service.add_member(db, token_payload, background_tasks, group_id, data)


@router.post('/add-members/{group_id}', status_code=status.HTTP_201_CREATED)
async def add_group_members(
    request: Request, 
    response: Response,
    token_payload: token_details,  
    db: db_dependency, 
    background_tasks: BackgroundTasks,
    group_id:int,
    data: schema.AddGroupMembers,
    ):
    return await group_service.add_members(db, token_payload, background_tasks, group_id, data)


@router.delete('/remove-member/{group_id}/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_group_member(
    request: Request, 
    response: Response,
    token_payload: token_details,
    db: db_dependency, 
    background_tasks: BackgroundTasks,
    user_id: int, 
    group_id: int,
    ):
    return await group_service.remove_member(db, token_payload, background_tasks, group_id, user_id)


@router.post('/remove-members/{group_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_group_members(
    request: Request, 
    response: Response,
    token_payload: token_details, 
    data: schema.RemoveGroupMembers, 
    db: db_dependency, 
    background_tasks: BackgroundTasks
    ):
    return await group_service.remove_members(db, data, token_payload, background_tasks)