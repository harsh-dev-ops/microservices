from fastapi import HTTPException, status


class InvalidPassword(HTTPException):
    def __init__(self, 
                 detail:str="Invalid Password", 
                 status_code = status.HTTP_406_NOT_ACCEPTABLE
                 ) -> None:
        super().__init__(status_code=status_code, detail=detail)


class InvalidEmailId(HTTPException):
    def __init__(self, 
                 detail: str="Email Id already exists!", 
                 status_code = status.HTTP_406_NOT_ACCEPTABLE
                 ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        

class MissingFormData(HTTPException):
    def __init__(self, 
                 detail: str="Missing form data!", 
                 status_code = status.HTTP_406_NOT_ACCEPTABLE
                 ) -> None:
        super().__init__(status_code=status_code, detail=detail)


class InvalidPhoneNumber(HTTPException):
    def __init__(self, 
                 detail: str="Invalid Phone Number!", 
                 status_code = status.HTTP_406_NOT_ACCEPTABLE
                 ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        
