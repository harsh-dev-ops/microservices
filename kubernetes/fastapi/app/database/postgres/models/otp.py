from datetime import datetime, timezone, timedelta
from .base import Base
from .users import User

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property, backref
from typing import List


class Otp(Base):
    __tablename__ = "otp"
    otp: Mapped[str] = mapped_column(sa.String(6), nullable=False)
    email_or_phone: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", backref=backref("otp", passive_deletes=True))
    expires_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc) + timedelta(minutes=2))
    
    @property
    def is_expired(self):
        expires_at = self.expires_at.replace(tzinfo=timezone.utc)
        return expires_at < datetime.now(timezone.utc)
    