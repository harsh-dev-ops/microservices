from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
import sqlalchemy as sa
from typing import List
from datetime import datetime, timedelta, timezone

from app.api.utils.strings import StringUtils

class UserMixin:
    
    @hybrid_property
    def password(self):
        if self.password == "" or self.password is None:
            return StringUtils.random_string(length=8)
        
    @hybrid_property
    def is_admin(self):
        if self.is_staff:
            return True
    
    @hybrid_property
    def is_verified(self):
        if self.is_staff:
            return True