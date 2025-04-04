import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property, backref
from typing import List
from datetime import datetime 
import enum
from uuid import uuid4

from .base import Base


class JWT(Base):
    __tablename__ = "jwt"
    access_key: Mapped[UUID] = mapped_column(UUID(as_uuid=True), index=True, default=uuid4, unique=True)
    refresh_key: Mapped[UUID] = mapped_column(UUID(as_uuid=True), index=True, default=uuid4, unique=True)
    refresh_token_exp_at: Mapped[datetime] = mapped_column(sa.DateTime)
    access_token_exp_at: Mapped[datetime]  = mapped_column(sa.DateTime)
    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", backref=backref("jwt", passive_deletes=True))
    