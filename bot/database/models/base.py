import re
from datetime import datetime
from typing import Annotated
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.declarative import declared_attr

def camel_to_snake_case(name: str) -> str:
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return pattern.sub("_", name).lower()

int_pk = Annotated[int, mapped_column(primary_key=True, index=True)]


class Base(DeclarativeBase):
    id: Mapped[int_pk]

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake_case(cls.__name__)


    
    repr_cols_num: int = 3  # print first columns
    repr_cols: tuple = ()  # extra printed columns

    def __repr__(self) -> str:
        cols = [
            f"{col}={getattr(self, col)}"
            for idx, col in enumerate(self.__table__.columns.keys())
            if col in self.repr_cols or idx < self.repr_cols_num
        ]
        return f"<{self.__class__.__name__} {', '.join(cols)}>"
