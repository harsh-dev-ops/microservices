import sqlalchemy as sa

from .crud_mixins import BaseCrudMixin
    

class BaseCRUD(BaseCrudMixin):
    def __init__(self, Model):
        self.Model = Model
        
    async def get_all(self, db, page=0, page_size=10):
        query = db.query(self.Model).filter().order_by(
            sa.desc(self.Model.updated_at))
        return self.pagination(query, page, page_size)
    
    async def create(self, db, data):
        obj = self.Model(**data)
        db.add(obj)
        db.commit()
        return obj
        
    async def create_many(self, db, data_list):
        obj_list = [self.Model(**data) for data in data_list]
        obj = db.add_all(obj_list)
        db.commit()
        return obj
    
    async def get(self, db, _id):
        obj = db.query(self.Model).filter(self.Model.id == _id).first()
        await self.missing_obj(obj, _id)
        return obj
    
    async def update(self, db, _id:int, data:dict):
        obj = db.query(self.Model).filter(self.Model.id == _id).first()
        await self.missing_obj(obj, _id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj
    
    async def delete(self, db, _id):
        obj = db.query(self.Model).filter(self.Model.id == _id).first()
        await self.missing_obj(obj, _id)
        if obj:
            db.delete(obj)
            db.commit()

