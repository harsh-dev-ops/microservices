from typing import Annotated
from typing_extensions import Doc
from pydantic import BaseModel

class Token(BaseModel):
    access_token: Annotated[str, Doc("")]
    token_type: Annotated[str, Doc("")]