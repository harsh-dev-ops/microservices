from numpy import roll
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property, backref
from typing import List
import enum

from .base import Base
from .users import User


class Group(Base):
    __tablename__ = "groups"
    name: Mapped[str] = mapped_column(sa.String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(sa.Text, default="")
    members: Mapped[List["User"]] = relationship("User", secondary="user_groups", backref=backref("groups", passive_deletes=True))


class RoleEnum(enum.Enum):
    admin = "admin"
    sub_admin = "sub_admin"
    manager = "manager"
    staff = "staff"
    member = "member"


class UserGroups(Base):
    __tablename__ = "user_groups"
    role: Mapped[str] = mapped_column(sa.Enum(RoleEnum), default=RoleEnum.member.value, nullable=False)
    add_members: Mapped[bool] = mapped_column(sa.Boolean(), default=False, nullable=False)
    view_members: Mapped[bool] = mapped_column(sa.Boolean(), default=False, nullable=False)
    remove_members: Mapped[bool] = mapped_column(sa.Boolean(), default=False, nullable=False)
    edit_members: Mapped[bool] = mapped_column(sa.Boolean(), default=False, nullable=False)
    edit_roles: Mapped[bool] = mapped_column(sa.Boolean(), default=False, nullable=False)
    buy_subscription: Mapped[bool] = mapped_column(sa.Boolean(), default=False, nullable=False)
    edit_subscription: Mapped[bool] = mapped_column(sa.Boolean(), default=False, nullable=False)
    view_subscription: Mapped[bool] = mapped_column(sa.Boolean(), default=False, nullable=False)
    edit_group: Mapped[bool] = mapped_column(sa.Boolean(), default=False, nullable=False)
    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user: Mapped["User"] = relationship("User", backref=backref("user_groups", passive_deletes=True),  overlaps="groups,groups,users,users")
    group_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("groups.id", ondelete='CASCADE'), nullable=False)
    group: Mapped["Group"] = relationship("Group", backref=backref("user_groups", passive_deletes=True), overlaps="groups,groups,users,users")