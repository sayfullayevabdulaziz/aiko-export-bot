# ruff: noqa: TCH001, TCH003, A003, F821
from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.database.models.base import Base


class UserModel(Base):
    user_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True, nullable=False)
    first_name: Mapped[str]
    phone: Mapped[str | None]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    language_code: Mapped[str | None]
    referrer: Mapped[str | None]
    
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_suspicious: Mapped[bool] = mapped_column(default=False)
    is_block: Mapped[bool] = mapped_column(default=False)
    is_premium: Mapped[bool] = mapped_column(default=False)

class ManagerModel(Base):
    name: Mapped[str]
    phone: Mapped[str] = mapped_column(sa.String(13), index=True, unique=True, nullable=False)
    login: Mapped[str] = mapped_column(sa.String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    active: Mapped[bool] = mapped_column(default=True)
    # fs_uniquifier: Mapped[str] = mapped_column(sa.String(255), unique=True,) # db.Column(db.String(255), unique=True)

# class ManagerModel(db.Model, UserMixin):
#     __tablename__ = "manager_model"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     phone = db.Column(db.String(13), index=True, unique=True, nullable=False)
#     login = db.Column(db.String(255), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)

#     active = db.Column(db.Boolean(), default=True)
#     # confirmed_at = db.Column(db.DateTime(), default=datetime.now())

#     def __str__(self) -> str:
#         return self.name


class ClientModel(Base):
    name: Mapped[str]
    phone: Mapped[str] = mapped_column(sa.String(13), index=True, unique=True, nullable=False)
    manager_id: Mapped[int] = mapped_column(sa.ForeignKey("manager_model.id"), nullable=False)
    active: Mapped[bool] = mapped_column(default=True)

    manager: Mapped["ManagerModel"] = relationship(backref='clients', lazy='joined')
