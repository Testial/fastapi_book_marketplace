from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String
from src.models.base import BaseModel
from src.models.books import Book

class Seller(BaseModel):
    __tablename__ = "sellers_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    e_mail: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    
    books: Mapped[list[Book]] = relationship("Book", backref="seller", lazy="selectin")
    books: Mapped[list[Book]] = relationship(back_populates="seller")