import os
import re as regex
from passlib.context import CryptContext
from passlib.hash import sha256_crypt, pbkdf2_sha256

from app.api.utils.strings import StringUtils

from .exceptions import Invalid
from app.conf.settings import settings
from app.database.postgres.models import User as UserModel
from app.database.postgres.crud import UserCrud


class GroupHelper:

    def __init__(self) -> None:
        pass 

class RoleHelper:

    def __init__(self) -> None:
        pass

class PermissionHelper:

    def __init__(self) -> None:
        pass
    
    async def get_permissions(self, role:str) -> list:
        all_permissions = ["add_members", "view_members", "remove_members", "edit_members", "edit_roles", "buy_subscription", "edit_subscription", "view_subscription", "edit_group"]
        if role == "admin":
            return all_permissions
        elif role == "sub_admin":
            return ["add_members", "view_members", "remove_members", "edit_members", "edit_roles", "buy_subscription", "view_subscription", "edit_group"]
        elif role == "manager":
            return ["add_members", "view_members", "remove_members", "edit_members",]
        elif role == "member":
            return ["view_members"]
        else:
            raise Invalid("Invalid Role!")