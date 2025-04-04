from fastapi import HTTPException


class BaseMixin:
    def missing_obj(self, obj):
        if not obj:
            raise HTTPException(detail=f"Object not found!", status_code=404)