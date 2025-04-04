from .users import UserCrud
from .otp import OtpCrud
from .groups import GroupCrud, UserGroups
from .jwt import JwtCrud


def get(cls_name:str):
    obj = dict(
        user_crud=UserCrud(), 
        otp_crud=OtpCrud(),
        group_crud=GroupCrud(),
        user_groups=UserGroups(),
        jwt_crud=JwtCrud()
        )
    return obj[cls_name]