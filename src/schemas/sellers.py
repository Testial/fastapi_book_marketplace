from pydantic import BaseModel, EmailStr
from typing import List, Optional
from src.schemas.books import ReturnedBookForSeller

__all__ = [
    "SellerCreate", "SellerUpdate", "SellerOut", "SellerOutWithBooks"
]

class SellerCreate(BaseModel):
    first_name: str
    last_name: str
    e_mail: EmailStr
    password: str

class SellerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    e_mail: Optional[EmailStr] = None

class SellerOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    e_mail: EmailStr

class SellerOutWithBooks(SellerOut):
    books: List[ReturnedBookForSeller] = []
