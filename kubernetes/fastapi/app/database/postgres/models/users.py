import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property, backref
from typing import List
import enum

from .base import Base


class User(Base):
    __tablename__ = "users"
    first_name: Mapped[str] = mapped_column(sa.String(50), default="")
    middle_name: Mapped[str] = mapped_column(sa.String(50), default="")
    last_name: Mapped[str] = mapped_column(sa.String(50), default="")
    full_name: Mapped[str] = mapped_column(sa.String(150), default="", onupdate=f"{first_name} {middle_name} {last_name}")
    email: Mapped[str] = mapped_column(sa.String(50), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(sa.String(250), nullable=True)
    phone: Mapped[str] = mapped_column(sa.String(15), unique=True, nullable=True)
    superuser: Mapped[bool] = mapped_column(sa.Boolean(), default=False, nullable=True)
    is_email_verified: Mapped[bool] = mapped_column(sa.Boolean(), default=False, nullable=True)
    is_phone_verified: Mapped[bool] = mapped_column(sa.Boolean(), default=False, nullable=True)
    is_verified: Mapped[bool] = mapped_column(sa.Boolean(), default=False, onupdate=True if is_email_verified or is_phone_verified else False)
    group: Mapped[List["Group"]] = relationship("Group", secondary="user_groups", backref=backref("users", passive_deletes=True))
    membership: Mapped[List["UserGroups"]] = relationship("UserGroups", backref=backref("users", passive_deletes=True))

