from fastapi import HTTPException, status


class Invalid(HTTPException):
    def __init__(self, 
                 detail:str="Invalid", 
                 status_code = status.HTTP_406_NOT_ACCEPTABLE
                 ) -> None:
        super().__init__(status_code=status_code, detail=detail)


class InsufficientPermissions(HTTPException):
    def __init__(self, 
                 detail:str="User has insufficient permission. Please Upgrade your role.", 
                 status_code = status.HTTP_403_FORBIDDEN
                 ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        

class GroupException(HTTPException):
    def __init__(self, 
                 detail:str="User already in 3 groups!", 
                 status_code = status.HTTP_406_NOT_ACCEPTABLE
                 ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        

class UserAlreadyHasRole(HTTPException):
    def __init__(self, 
                 detail:str="User already has role! Please try again.",
                 status_code = status.HTTP_406_NOT_ACCEPTABLE
                 ) -> None:
        super().__init__(status_code=status_code, detail=detail)