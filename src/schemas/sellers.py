from pydantic import (
    BaseModel, EmailStr, Field, SecretStr, field_validator
)
from pydantic_core import PydanticCustomError
from password_validator import PasswordValidator
from icecream import ic
from .books import ReturnedBookLinkedToSeller

__all__ = ['RegisteringSeller', 'ReturnedSeller', 'ReturnedAllSellers', 'ReturnedSellerWithBooks']

class BaseSeller(BaseModel):
    first_name: str
    last_name: str

class RegisteringSeller(BaseSeller):
    password: str
    e_mail: EmailStr
    @field_validator('password')
    @staticmethod
    def validate_password(password):
        ic(password)
        schema = PasswordValidator()
        schema.min(8).max(64)\
            .has().uppercase()\
            .has().lowercase()\
            .has().digits()\
            .has().no().spaces()
        if not schema.validate(password):
            raise PydanticCustomError('Validation error', 'Password should be in common format!')
        return password

class ReturnedSeller(BaseSeller):
    e_mail: EmailStr
    id: int

class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]

class ReturnedSellerWithBooks(BaseSeller):
    id: int
    e_mail: EmailStr = Field(alias="email")
    books: list["ReturnedBookLinkedToSeller"]
    model_config = {
        "populate_by_name": True,
    }
    