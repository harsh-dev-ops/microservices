# from sqlalchemy.orm import Session

# from ..models.users import User
# from .base import BaseCRUD
# from ..models import Token


# class TokenCRUD(BaseCRUD):
#     def __init__(self, Model=Token):
#         super().__init__(Model)
    
#     async def get_by_token(self, db:Session, token:str) -> Token:
#         obj = db.query(self.Model).filter(self.Model.token == token).first()
#         return obj