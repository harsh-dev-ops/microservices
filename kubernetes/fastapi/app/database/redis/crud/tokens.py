from .base import BaseCrud
from ..models import TokenModel

class TokenCrud(BaseCrud):
    def __init__(self, Model=TokenModel):
        super().__init__(Model)
        
    def get_by_user_id(self, user_id:str):
        obj = self.Model.find(self.Model.user_id==user_id).all()
        return obj
    
    def get_by_access_key(self, access_key:str, user_id:str):
        try: 
            obj = self.Model.find(
                (TokenModel.access_key==access_key) & (TokenModel.user_id==user_id)
            ).first()
            self.missing_obj(obj)
            return obj
        except Exception as e:
            print(e)

    def get_by_refresh_key(self, refresh_key:str, user_id:str):
        try: 
            obj = self.Model.find(
                (TokenModel.refresh_key==refresh_key) & (TokenModel.user_id==user_id)
            ).first()
            self.missing_obj(obj)
            return obj
        except Exception as e:
            print(e)