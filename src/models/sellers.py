from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from .base import BaseModel


if TYPE_CHECKING:
    from .books import Book

class Seller(BaseModel):
    __tablename__ = 'sellers_table'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(32), nullable=False)
    last_name: Mapped[str] = mapped_column(String(32), nullable=False)
    e_mail: Mapped[str] = mapped_column(String(64), nullable=False)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    books: Mapped[List["Book"]] = relationship(back_populates="seller", cascade="all, delete-orphan")
    