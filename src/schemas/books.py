from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from pydantic_core import PydanticCustomError


__all__ = ["IncomingBook", "ReturnedBook", "ReturnedAllBooks", "SellerBook"]


class BaseBook(BaseModel):
    title: str
    author: str
    year: int


class IncomingBook(BaseBook):
    pages: int = Field(default=150, alias="count_pages")
    seller_id: int

    @field_validator("year")
    @staticmethod
    def validate_year(val: int) -> int:
        if val < 2020:
            raise PydanticCustomError(
                error_type="Valdation error",
                message_template="Year is too old",
            )
        return val


class ReturnedBook(BaseBook):
    id: int
    pages: int
    seller_id: int

    model_config = {"from_attributes": True}


class SellerBook(BaseBook):
    id: int
    pages: int

    model_config = {"from_attributes": True}


class ReturnedAllBooks(BaseModel):
    books: list[ReturnedBook]
