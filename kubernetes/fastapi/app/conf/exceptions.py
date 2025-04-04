from fastapi import HTTPException, status


class MethodDepericated(HTTPException):
    def __init__(self, 
                 detail: str="Method has beed depericated!", 
                 status_code: int = status.HTTP_403_FORBIDDEN
                 ) -> None:
        super().__init__(status_code=status_code, detail=detail)