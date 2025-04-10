from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError

__all__ = ["IncomingBook", "ReturnedBook", "ReturnedAllbooks", "ReturnedBookLinkedToSeller"]


class BaseBook(BaseModel):
    title: str
    author: str
    year: int

class IncomingBook(BaseBook):
    seller_id: int
    pages: int = Field(
        default=150, alias="count_pages"
    ) 

    @field_validator("year")
    @staticmethod
    def validate_year(val: int):
        if val < 2020:
            raise PydanticCustomError("Validation error", "Year is too old!")
        return val

class ReturnedBook(BaseBook):
    id: int
    pages: int
    seller_id: int


class ReturnedAllbooks(BaseModel):
    books: list[ReturnedBook]

class ReturnedBookLinkedToSeller(BaseBook):
    id: int
    pages: int = Field(alias="count_pages")
    model_config = {
        "populate_by_name": True,
    }
