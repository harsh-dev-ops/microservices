from fastapi import HTTPException
import sqlalchemy as sa

class BaseCrudMixin:
    async def __init__(self, Model):
        self.Model = Model
    
    async def missing_obj(self, obj, _id:int | str | None = None):
        if obj is None:
            raise HTTPException(detail=f"Object with id: {_id} not found!", status_code=404)
        
    async def pagination(self, query, page:int = 0, page_size:int = 10):
        if page_size:
            query = query.limit(page_size)
        if page:
            query = query.offset(page*page_size)
        return query.all()
    
    async def search(self, db, query: str, page:int=0, page_size:int=20):
        search_objects = db.query(
            self.Model.name.like(f'%{query}%'))
        return self.pagination(search_objects, page, page_size)
    
    async def vector_search(self, db, query:str, page: int=0, page_size:int=30):
        results = db.query(self.Model).filter(self.Model.search_vector.match(query))
        return self.pagination(results, page, page_size)