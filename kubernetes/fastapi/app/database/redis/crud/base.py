from redis_om import NotFoundError
from ..models import TokenModel

from .mixins import BaseMixin

class BaseCrud(BaseMixin):
    def __init__(self, Model):
        self.Model = Model
    
    def get(self, pk:str):
        obj = self.Model.get(pk)
        self.missing_obj(obj)
        return obj
    
    def delete(self, pk:str):
        self.Model.delete(pk)
    
    def create(self, data:dict):
        obj = self.Model(**data)
        obj.save()
        return obj
    
    def update(self, data:dict, pk:str):
        obj = self.get(pk)
        for k, v in data.items():
            setattr(obj, k, v)
        obj.save()
        return obj
        