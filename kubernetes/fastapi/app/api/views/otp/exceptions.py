from fastapi import HTTPException, status


class InvalidOtp(HTTPException):
    def __init__(self, 
                 detail:str="Invalid Otp!", 
                 status_code = status.HTTP_406_NOT_ACCEPTABLE
                 ) -> None:
        super().__init__(status_code=status_code, detail=detail)