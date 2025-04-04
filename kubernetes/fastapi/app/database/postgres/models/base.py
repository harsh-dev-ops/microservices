from datetime import datetime
from pytz import UTC
from uuid import uuid4

import inflect
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR
# class TSVector(sa.types.TypeDecorator):
#     impl = TSVECTOR


@as_declarative()
class Base:
    id: Mapped[int]  = mapped_column(sa.Integer, primary_key=True, index=True, autoincrement=True)
    # uid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), index=True, default=uuid4, unique=True)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )
    __name__: str

    # Internal Method to generate table name
    def _generate_table_name(str):
        words = [[str[0]]]
        for c in str[1:]:
            if words[-1][-1].islower() and c.isupper():
                words.append(list(c))
            else:
                words[-1].append(c)
        return inflect.engine().plural(
            "_".join("".join(word) for word in words).lower()
        )

    # Generate __tablename__ automatically in plural form.
    #   
    # i.e 'myTable' model will generate table name 'my_tables'
    @declared_attr
    def __tablename__(cls) -> str:
        return cls._generate_table_name(cls.__name__)

