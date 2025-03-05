from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import BaseModel


class Book(BaseModel):
    __tablename__ = "books_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int]
    pages: Mapped[int]
    seller_id: Mapped[int] = mapped_column(
        ForeignKey("sellers_table.id", ondelete="CASCADE"),
        nullable=False,
    )
    seller: Mapped["Seller"] = relationship(back_populates="books")  # noqa: F821
