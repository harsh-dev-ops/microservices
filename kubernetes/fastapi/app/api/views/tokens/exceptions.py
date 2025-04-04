from fastapi import HTTPException, status



class TokenNotFound(HTTPException):
    def __init__(self, 
                 detail: str="Token Not Found in database!", 
                 status_code: int = status.HTTP_401_UNAUTHORIZED
                 ) -> None:
        super().__init__(status_code=status_code, detail=detail)


class TokenExpired(HTTPException):
    def __init__(self, 
                 detail: str="Token Expired!", 
                 status_code: int = status.HTTP_426_UPGRADE_REQUIRED
                 ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        
        
class InvalidToken(HTTPException):
    def __init__(self, 
                 detail: str="Invalid Token!", 
                 status_code = status.HTTP_401_UNAUTHORIZED
                 ) -> None:
        super().__init__(status_code=status_code, detail=detail)