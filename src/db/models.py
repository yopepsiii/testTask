from datetime import datetime
import uuid
from typing import List

from sqlalchemy import func, types, text, ForeignKey, select, Table, Column
from sqlalchemy.orm import (
    declarative_base,
    Mapped,
    mapped_column,
    relationship,
)

Base = declarative_base()


class User(Base):
    __tablename__ = "Users"

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid, server_default=text("gen_random_uuid()"), primary_key=True
    )

    username: Mapped[str] = mapped_column(nullable=True)

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )

    products: Mapped['Product'] = relationship(cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "Products"

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid, server_default=text("gen_random_uuid()"), primary_key=True
    )

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    width: Mapped[int] = mapped_column(nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)

    price: Mapped[float] = mapped_column(nullable=False)

    creator_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Users.id'))

    category_id: Mapped[int] = mapped_column(ForeignKey('Categories.id'))
    category: Mapped['Category'] = relationship(lazy='selectin')


class Category(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)